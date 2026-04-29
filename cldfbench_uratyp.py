import dataclasses
import re
import pathlib
import collections

from unidecode import unidecode
from nameparser import HumanName
from pybtex import database
from clld.lib.bibtex import unescape
from clldutils.misc import slug
from clldutils.text import split_text
from clldutils.markup import iter_markdown_tables
from csvw.dsv import reader
from cldfbench import Dataset as BaseDataset, CLDFSpec
from pycldf.sources import Source, Sources

from uratypcommands.cldfmd import References, cldf_md

GB_LANGUAGE_MAP = {
    #GB - UT
    # Central Mansi [cent2322]
    #Komi-Permyak [komi1269]
    # Ume Saami [umes1235]
    'gras1239': 'east2328',
    'kama1378': 'kama1351',
    'voro1241': 'sout2679',
    'west2392': 'kozy1238',
}


def read(p, **kw):
    return list(reader(p, dicts=True, **kw))


def gb_codes(s):
    s = s.replace('multistate', '').strip()
    for code in split_text(s, separators=',;'):
        n, label = code.strip().split(':')
        assert isinstance(int(n), int), s
        yield n.strip(), label.strip()


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "uratyp"

    def cldf_specs(self):  # A dataset must declare all CLDF sets it creates.
        return CLDFSpec(dir=self.cldf_dir, module="StructureDataset")

    def cmd_download(self, args):
        pass

    def _schema(self, args):
        args.writer.cldf.add_component(
            'LanguageTable',
            {
                'name': 'Source',
                'separator': ';',
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#source",
            },
            {
                'name': 'UT_Experts',
                'separator': ' ',
            },
            {
                'name': 'GB_Experts',
                'separator': ' ',
            },
        )
        args.writer.cldf.add_table(
            'contributors.csv',
            {
                'name': 'ID',
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#id",
            },
            {
                'name': 'Name',
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#name",
            },
        )
        args.writer.cldf.add_foreign_key('LanguageTable', 'UT_Experts', 'contributors.csv', 'ID')
        args.writer.cldf.add_foreign_key('LanguageTable', 'GB_Experts', 'contributors.csv', 'ID')
        args.writer.cldf.add_component('CodeTable')
        args.writer.cldf.add_component(
            'ExampleTable',
            {
                'name': 'Source',
                'separator': ';',
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#source",
            },
            'IPA',
            #'Original_Script',
        )
        t = args.writer.cldf.add_component('ContributionTable')
        t.common_props['dc:description'] = \
            "UraTyp combines typological data collected with two separate questionnaires. " \
            "These questionnaires are listed in the ContributionTable, and parameters, " \
            "i.e. features (and thus values) are linked to this table according to their origin."
        t = args.writer.cldf.add_component(
            'ParameterTable',
            'Area',
            {
                "name": "Contribution_ID",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#contributionReference",
                "dc:description": "Links a feature to the questionnaire it comes from.",
            },
            {
                "name": "Feature_Description",
                "dc:format": "text/markdown",
                "dc:conformsTo": "CLDF Markdown",
            },
            {
                "name": "Source",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#source",
                "dc:description": "Sources cited in the feature description.",
                "separator": ";",
            }
        )
        args.writer.cldf['LanguageTable', 'Glottocode'].null = ['?']
        args.writer.cldf['LanguageTable', 'ISO639P3code'].null = ['?']
        # args.writer.cldf['LanguageTable', 'Macroarea'].null = ['Eurasia']
        args.writer.cldf.add_columns('LanguageTable', 'Subfamily')
        args.writer.cldf.add_columns(
            'ValueTable',
            'Source_Comment',
            {
                'name': 'Example_ID',
                'separator': ' ',
                'propertyUrl': 'http://cldf.clld.org/v1.0/terms.rdf#exampleReference'})

    def cmd_makecldf(self, args):
        args.writer.cldf.properties['dc:description'] = self.dir.joinpath('README.md').read_text(encoding='utf8')
        bibdata = database.parse_file(str(self.raw_dir.joinpath('sources.bib')))
        refs_by_lid = collections.defaultdict(list)
        refkeys = {}
        for key, entry in bibdata.entries.items():
            src = Source.from_entry(key, entry)
            for k in src:
                src[k] = unescape(src[k])
            for lid in src.get('langref', '').split(','):
                lid = lid.strip()
                if lid:
                    refs_by_lid[lid].append(src.id)
            rk = src.get('key')
            if not rk:
                rk = src.refkey(year_brackets=None)
            assert rk not in refkeys, (rk, src)
            refkeys[rk] = src.id
            args.writer.cldf.sources.add(src)
        refkeys['Aikio 2009'] = refkeys['Aikio and Ylikoski 2009']

        self._schema(args)

        lmap, lomap = {}, {}
        for lang in self.raw_dir.read_csv('Languages.csv', dicts=True):
            lang['ISO639P3code'] = lang.pop('ISO.639.3')
            #lang['Source'] = refs.get(lang['Name'], [])
            del lang['citations']
            args.writer.objects['LanguageTable'].append(lang)
            lmap[lang['Name']] = lang['ID']
            lmap[unidecode(lang['Name'])] = lang['ID']
            lmap[lang['Glottocode']] = lang['ID']
            lomap[lang['ID']] = lang

        data = Data.from_repos(self.raw_dir, lmap, refkeys, args.log)

        t = list(iter_markdown_tables(self.dir.joinpath('CONTRIBUTORS.md').read_text(encoding='utf8')))
        experts = collections.defaultdict(lambda: collections.defaultdict(list))
        for row in t[1][1]:
            row = list(zip(t[1][0], row))
            contrib, lid = None, None
            for k, v in row:
                if k == 'Language':
                    lid = lmap[unidecode(v).replace(' ', '_').replace('-', '_')]
                if k in ['UT', 'GB']:
                    contrib = k
                if k == 'Values and/or examples':
                    for e in v.split(','):
                        e = e.strip()
                        if e:
                            n = HumanName(e)
                            cid = slug('{}{}{}'.format(n.middle, n.last, n.first))
                            if cid:
                                experts[lid][contrib].append((cid, e))
        cids = set()
        for lang in args.writer.objects['LanguageTable']:
            if lang['ID'] in experts:
                for contrib in ['GB', 'UT']:
                    if contrib in experts[lang['ID']]:
                        lang['{}_Experts'.format(contrib)] = []
                        for cid, name in experts[lang['ID']][contrib]:
                            if cid not in cids:
                                args.writer.objects['contributors.csv'].append(dict(ID=cid, Name=name))
                                cids.add(cid)
                            lang['{}_Experts'.format(contrib)].append(cid)

        gb_features = {
            r['Feature_ID']: list(gb_codes(r['Possible Values']))
            for r in self.raw_dir.read_csv('gb.csv', dicts=True)}

        refs = References.from_sources(args.writer.cldf.sources)
        for sd, contrib in [('UT', 'Uralic Areal Typology'), ('GB', 'Grambank')]:
            args.writer.objects['ContributionTable'].append(
                dict(ID=sd, Name=contrib))

            for param in read(self.raw_dir / sd / 'Features.csv'):
                param['Contribution_ID'] = sd
                doc = self.cldf_dir / '..' / 'doc' / '{}.md'.format(param['ID'])
                if doc.exists():
                    param['Feature_Description'], param['Source'] = cldf_md(doc, refs)
                args.writer.objects['ParameterTable'].append(param)
                if sd == 'UT':
                    codes = [('1', 'yes'), ('0', 'no')]
                else:
                    codes = gb_features[param['ID']]
                for code, name in codes:
                    args.writer.objects['CodeTable'].append(dict(
                        ID='{}-{}'.format(param['ID'], code),
                        Name=code,
                        Description=name,
                        Parameter_ID=param['ID'],
                    ))

        #
        # Fill ExampleTable and ValueTable with the data aggregated in data!
        #
        eids, pk = collections.defaultdict(list), 0
        for (lid, eid), exs in data.examples.items():
            for ex in exs:
                refs_by_lid[lid].extend([Sources.parse(ref)[0] for ref in ex.Source])
                pk += 1
                eids[(lid, eid)].append(pk)
                args.writer.objects['ExampleTable'].append(dict(
                    ID=str(pk),
                    Language_ID=lmap[lid],
                    Primary_Text=ex.Primary_Text.replace('-', ''),
                    Analyzed_Word=ex.Analyzed,
                    Gloss=ex.Gloss,
                    Translated_Text=ex.Translation or None,
                    IPA=ex.IPA,
                    Source=ex.Source,
                ))

        for lid, vv in data.values.items():
            for fid, v in vv.items():
                exs = []
                for eid in v.Example:
                    if (lid, eid) in eids:
                        exs.extend(eids[(lid, eid)])
                refs_by_lid[lid].extend([Sources.parse(ref)[0] for ref in v.Source])
                args.writer.objects['ValueTable'].append(dict(
                    ID='{}-{}'.format(lid, fid),
                    Language_ID=lmap[lid],
                    Parameter_ID=fid,
                    Value=None if v.Value == '?' else v.Value,
                    Code_ID=None if v.Value == '?' else f'{fid}-{v.Value}',
                    Comment=v.Comment,
                    Example_ID=[str(pk) for pk in sorted(set(exs))],
                    Source=v.Source,
                    Source_Comment="; ".join(v.SourceComment),
                ))
        for lid, srcids in refs_by_lid.items():
            lomap[lmap[lid]]['Source'] = sorted(set(srcids))


def _checked_sources(s, refkeys, what, log):
    refpattern = re.compile(r'({})(\:\s*([0-9, f§XIV\-]+|in passim|[^\s]+))?'.format('|'.join(re.escape(k) for k in refkeys)))

    s = re.sub(r'\s+', ' ', s)

    res = {'Source': [], 'SourceComment': []}
    for src in s.split(';'):
        src = src.strip()
        if src:
            if ('p.c. ' in src) or ('p.c.)' in src) or ('p. c.' in src):
                res['SourceComment'].append(src)
                continue

            if refpattern.fullmatch(src):
                key, _, pages = src.partition(':')
                s = refkeys[key.strip()]
                if pages:
                    s += f"[{pages.replace('[', '(').replace(']', ')')}]"
                res['Source'].append(s)
                continue

            if ':' in src:
                refkey, _, pages = src.partition(':')
                if refkey.strip() in refkeys and (
                        re.fullmatch(r'[^\s]+(,\s([^\s]+|in passim))+', pages.strip()) or
                        what == 'example'):
                    s = refkeys[refkey.strip()]
                    if pages:
                        s += f"[{pages.replace('[', '(').replace(']', ')')}]"
                    res['Source'].append(s)
                    continue

            log.warning('Ignoring %s reference: %s', what, src)
            res['SourceComment'].append(src)
    return res


@dataclasses.dataclass
class DataRow:
    ID: str
    Feature: str
    Value: str
    Source: list[str]
    Example: list[str]
    Comment: str
    SourceComment: str = ''

    @classmethod
    def from_row(cls, fname, row, eids, invalid_eids, refkeys, log):
        assert re.fullmatch(r'(UT|GB)[0-9]+', row['ID'])
        assert row['Value'] in {'?', '0', '1', '2', '3'}, row
        row.update(_checked_sources(row['Source'], refkeys, 'value', log))
        row.update(cls._checked_example(row['Example'], eids, invalid_eids, fname))
        return cls(**row)

    @staticmethod
    def _checked_example(s, eids, invalid_eids, fname):
        res = {'Example': []}
        for ex in re.split(r'[.,;]', s):
            ex = ex.strip()
            if not ex:
                continue
            ex = ex.replace('FB', 'GB')
            ex = ex.replace('Ut', 'UT')
            ex = ex.replace(' ', '')
            ex = ex.replace('T-', 'T')
            ex = ex.replace('B-', 'B')
            ex = re.sub(r'G(?P<digit>[0-9])', lambda m: 'GB' + m.group('digit'), ex)
            assert re.fullmatch(r'(UT|GB)[0-9]{3}(-[0-9]+)?', ex), s
            #
            # FIXME: The below check may fail in case of invalid examples!
            #
            if (fname, ex) in invalid_eids:
                continue
            assert ex in eids, (fname, s)
            res['Example'].append(ex)
        return res


def _align(s1, s2):
    import itertools
    t1, t2 = [], []
    for c1, c2 in itertools.zip_longest(s1, s2, fillvalue=''):
        t1.append(c1.ljust(max([len(c1), len(c2)])))
        t2.append(c2.ljust(max([len(c1), len(c2)])))
    return f'{" ".join(t1)}\n{" ".join(t2)}'


@dataclasses.dataclass
class ExampleRow:
    ID: str
    Primary_Text: str
    IPA: str
    Analyzed: list[str]
    Gloss: list[str]
    Translation: str
    Example_Source: str
    Comment: str = ''
    Source: list[str] = dataclasses.field(default_factory=[])
    SourceComment: str = ''

    @staticmethod
    def split_colon(items):
        res = []
        for item in items:
            if item != ':' and item.endswith(':'):
                res.extend([item[:-1], ':'])
            else:
                res.append(item)
        return res

    @staticmethod
    def is_list(items):
        return len(items) > 1 and all(item.endswith(',') for item in items[:-1])

    @classmethod
    def from_row(cls, row, refkeys, sd, pname, log):
        row.update(_checked_sources(row['Example_Source'], refkeys, 'example', log))

        row['Analyzed'] = row['Analyzed'].split()
        row['Gloss'] = row['Gloss'].split()

        if not row['Primary_Text']:
            if row['Analyzed']:
                row['Primary_Text'] = ' '.join(row['Analyzed']).replace('-', '')

        if row['Primary_Text']:
            if row['Gloss'] and not row['Analyzed']:
                row['Analyzed'] = row['Primary_Text'].split()

            if row['Analyzed'] and row['Gloss']:
                a = row['Analyzed']
                g = row['Gloss']
                if len(a) != len(g):
                    if a[-1] == '…':
                        a = a[:-1]
                        assert len(a) == len(g), f'misaligned example: {row}'
                        row['Gloss'].append('…')
                    elif len(row['Analyzed']) == 1 and cls.is_list(row['Gloss']):
                        row['Gloss'] = [';'.join(item.replace(',', '') for item in row['Gloss'])]
                    elif len(cls.split_colon(a)) == len(cls.split_colon(g)):
                        row['Analyzed'] = cls.split_colon(row['Analyzed'])
                        row['Gloss'] = cls.split_colon(row['Gloss'])
                    else:
                        print(f'{sd}/language-tables/{pname}:{row['ID']}')
                        print(_align(row['Analyzed'], row['Gloss']))
                        log.error('misaligned %s \n%s', row['Primary_Text'], _align(row['Analyzed'], row['Gloss']))
                        return None

            if len(row['Analyzed']) != len(row['Gloss']):
                if not row['Gloss']:
                    if len(row['Analyzed']) == 1 and row['Analyzed'][0] in {row['Primary_Text'], row['IPA']}:
                        row['Analyzed'] = []
                    elif ' '.join(row['Analyzed']) in {row['Primary_Text'], row['IPA']}:
                        row['Analyzed'] = []
                    else:
                        assert ' '.join(row['Analyzed']).replace('-', '') in {
                            row['Primary_Text'].replace('-', ''), row['IPA'].replace('-', '')}
                        row['Analyzed'] = []

                assert len(row['Analyzed']) == len(row['Gloss'])

            return cls(**row)
        assert not any(row[key] for key in {'Primary_Text', 'Analyzed', 'Gloss'})
        return None


@dataclasses.dataclass
class Data:
    values: dict[str, dict[str, DataRow]] = dataclasses.field(
        default_factory=lambda: collections.defaultdict(dict))
    examples: dict[tuple[str, str], list[ExampleRow]] = dataclasses.field(
        default_factory=lambda: collections.defaultdict(list))
    invalid_examples: set[tuple[str, str]] = dataclasses.field(default_factory=set)

    @staticmethod
    def norm_row(row, lmap):
        new = {}
        for k, v in row.items():
            k = k.strip()
            v = v.strip()
            if k in {'x', 'y'}:
                continue
            if lmap.get(k.replace('.', '_')):
                k = 'Value'
            elif k == 'Name':
                k = 'Feature'
            v = v.replace('\xa0', ' ')
            v = re.sub(r'\s+', ' ', v)
            new[k] = v
        return new

    @staticmethod
    def _iter_rows(d, what, lmap):
        glob = '*_examples.csv' if what == 'examples' else '*.csv'
        for p in sorted(d.glob(glob), key=lambda p_: p_.stem):
            if what != 'examples' and p.stem.endswith('_examples'):
                continue
            for row in reader(p, dicts=True):
                yield p, Data.norm_row(row, lmap)

    @classmethod
    def from_repos(cls, raw_dir, lmap, refkeys, log):
        for key in list(refkeys):
            if ' and ' in key:
                refkeys[key.replace(' and ', ' & ')] = refkeys[key]
            if ' & ' in key:
                refkeys[key.replace(' & ', ' and ')] = refkeys[key]
        res = cls()
        for sd in ['UT', 'GB']:
            eids = set()
            for p, row in cls._iter_rows(raw_dir / sd / 'language-tables', 'examples', lmap):
                ex = ExampleRow.from_row(row, refkeys, sd, p.name, log)
                if ex:
                    res.examples[p.stem.replace('_examples', ''), row['ID']].append(ex)
                    eids.add(row['ID'])
                else:
                    res.invalid_examples.add((p.stem.replace('_examples', ''), row['ID']))

            for p, row in cls._iter_rows(raw_dir / sd / 'language-tables', 'values', lmap):
                try:
                    assert row['ID'] not in res.values[p.stem], f"Duplicate: {p.stem}:{row['ID']}"
                    res.values[p.stem][row['ID']] = DataRow.from_row(p.stem, row, eids, res.invalid_examples, refkeys, log)
                except KeyError as e:
                    raise ValueError(p) from e

        return res

    def stats(self):
        return (len(self.values), sum(len(self.values[s]) for s in self.values), len(self.examples), len(self.invalid_examples))
