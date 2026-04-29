"""
UT116-120,123,133,134,140,146,147,154,157,165,166,
just a word
UT121-166

"""
import re
import collections
import dataclasses
import urllib.parse

from pycldf import Sources


@dataclasses.dataclass
class References:
    sources: Sources
    keys: dict[str, str]
    regexes: dict[str, re.Pattern]
    count_links: int = 0
    matched: set = dataclasses.field(default_factory=set)

    @property
    def missed(self):
        return [srcid for srcid in self.keys.values() if srcid not in self.matched]

    @classmethod
    def from_sources(cls, sources):
        keys = {s.get('key') or s.refkey(year_brackets=None): s.id for s in sources}
        return cls(sources, keys, {k: cls.key_to_regex(k) for k in keys})

    @staticmethod
    def key_to_regex(key):
        key = key.replace('(in preparation)', 'n.d.').strip()
        comps = key.split()
        if len(comps) > 1:
            authors = r'\s+'.join(
                [re.escape(c) if c not in {'&', 'and'} else r'(and|&)' for c in comps[:-1]])
            year = comps[-1]
            try:
                return re.compile(r"{}(['’]s?)?(,\s*eds?,\s*)?\s*\(?{}".format(authors, year))
            except:
                raise ValueError(key)
        return re.compile(r"\(({})\)".format(comps[0]))

    def repl(self, key, sid, s):
        def link(label, srcid):
            return '('.join(
                '[{}](sources.bib?label={}#cldf:{})'.format(s, urllib.parse.quote_plus(s), srcid)
                for s in label.split('('))

        yp = re.compile(r'[,;]\s+(?P<label>[0-9]{4}([ab])?)\s*')
        rem = s
        m = self.regexes[key].search(rem)
        while m:
            yield m.string[:m.start()], None
            ms = m.string[m.start():m.end()]
            rem = m.string[m.end():]

            if re.match(r'[^<]+</a>', rem):
                # We are already in a link!
                yield ms, None
                m = self.regexes[key].search(rem)
                continue

            yield link(ms, sid), sid
            if '(' in ms and not rem.startswith(')'):
                mm = yp.match(rem)
                while mm:
                    kk = f"{' '.join(key.split()[:-1])} {mm.group('label')}"
                    if kk in self.keys:
                        yield "; " + link(mm.group('label'), self.keys[kk]), self.keys[kk]
                    else:
                        yield "; " + mm.group('label'), None
                    rem = rem[mm.end():]
                    mm = yp.match(rem)

            m = self.regexes[key].search(rem)
        yield rem, None

    def link(self, s):
        s = s.replace('‑', '-')
        s = s.replace('-', '-')
        s = s.replace('ẞ', 'ß')
        for k, v in {
        }.items():
            s = s.replace(k, v)
        r = s
        refs = set()
        for key, sid in sorted(self.keys.items(), key=lambda i: -len(i[0])):
            r_ = []
            for t, srcid in self.repl(key, sid, r):
                r_.append(t)
                if srcid:
                    self.count_links += 1
                    self.matched.add(srcid)
                    refs.add(srcid)
            r = ''.join(r_)
        return r, sorted(refs)


def run(args):
    from cldfbench_uratyp import Dataset
    ds = Dataset()
    refs = References.from_sources(ds.cldf_reader().sources)
    for p in sorted(ds.dir.joinpath('doc').glob('*.md'), key=lambda pp: int(pp.stem[2:])):
        md, cited = cldf_md(p, refs)
        print('---\n', p.name, '\n---')
        print(md)
        print(cited)


H_PATTERN = re.compile(r'\*\*(?P<title>[^*]+)\*\*')
EXNUM_PATTERN = re.compile(r'>?\((?P<num>[0-9]+)\)')


def cldf_md(p, refs):
    """
   **Is there a distinct category of dual for verbal agreement with a dual subject?**

Dual is a grammatical number category that refers to two entities. This question asks whether there is agreement, i.e., that in addition to being märked on the subject, dual is also marked on the verb, as in the South Saami example (1).

(1) South Saami<br/>
>*Månnoeh luhkien*<br/>
>we.1DU read.1DU<br/>
>‘We two read'

Agreement may be consistent for various kinds of nouns (e.g., animate and inanimate nouns) and pronouns. In South Saami, there is dual agreement only for pronouns. In other instances, the plural form is used (cf. examples 2-3).<br/>

(1) Tundra Nenets<br/>
>a. *xadaəda*<br/>
>xadaə-da<br/>
>kill-3SG>SG.OBJ<br/>
>‘He killed him/her’<br/>

>b. *xadaŋaxəyuda*<br/>
>xadaŋa-xəyu-da<br/>
>kill-DU.OBJ-3SG<br/>
>‘He killed them two’<br/>
(Nikolaeva 2014:80)


(2) South Saami<br/>
>*Maanah låhkijägan*<br/>
>child.PL read.3DU<br/>
>‘Children (= two) read'

(3) South Saami<br/>
>*Göökte  gaahtoeh  byöpmedieh*<br/>
>two      cat.PL    eat.3PL<br/>
>‘Two cats eat'

**Coding.** The value is ‘1’ if there is verbal agreement with a dual subject in at least one of the possibilities mentioned above. The answer is ‘0’ if dual is marked only on the verb or only on the noun.</p>

    :param text:
    :return:
    """
    fid = int(p.stem[2:])
    text = p.read_text(encoding='utf8')
    title = None
    in_refs = False
    nrefs = 0
    cited = set()
    lines = []

    for i, line in enumerate(text.strip().split('\n')):
        m = H_PATTERN.match(line)
        if m:
            content = m.group('title').strip()
            rem = m.string[m.end():].strip()
            if content.endswith('.'):
                content = content[:-1].strip()
            if not title:
                assert i == 0
                assert not rem
                title = content
            else:
                if content == 'References':
                    in_refs = True
                else:
                    lines.append(f'## {content}\n')
                    if rem and rem != '<br/>':
                        line, rs = refs.link(line)
                        cited |= set(rs)
                        lines.append(rem)
            continue

        if line.strip() == '<br/>':
            lines.append('')
            continue
        if in_refs and line.strip():
            nrefs += 1
        else:
            line, rs = refs.link(line)
            cited |= set(rs)
            lines.append(line)

    assert len(cited) >= nrefs, (p.name, cited, nrefs)
    return '\n'.join(lines), sorted(cited)
