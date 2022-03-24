import re
import pathlib
import collections

from unidecode import unidecode
from nameparser import HumanName
from pybtex import database
from clld.lib.bibtex import unescape
from clldutils.misc import slug
from clldutils.text import split_text, split_text_with_context
from clldutils.markup import iter_markdown_tables
from csvw.dsv import reader
from cldfbench import Dataset as BaseDataset, CLDFSpec
from pycldf.sources import Source

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


def fix_internal_stress(s):
    import unicodedata

    def is_letter(c):
        return c and unicodedata.category(c)[0] == 'L'

    new, last = [], None
    for i, c in enumerate(s):
        next = s[i + 1] if i + 1 < len(s) else None
        if c == "'" and is_letter(next) and is_letter(last):
            c = '\u02c8'
        new.append(c)
        last = c
    return ''.join(new)


NA = ['?', '0?', '1?', '?1', '!!', '?CHECK, possibly 0',
      '?CHECK, possibly 1', '?CHECK']


def checkex(row):
    if row['Primary_Text']:
        if row['Analyzed'] and row['Gloss']:
            a = row['Analyzed'].strip().split()
            g = row['Gloss'].strip().split()
            if len(a) != len(g):
                return False
        return True
    return False


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
            'Original_Script',
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
                "dc:description": "Relative path to a markdown document describing the feature",
            }
        )
        args.writer.cldf['LanguageTable', 'Glottocode'].null = ['?']
        args.writer.cldf['LanguageTable', 'ISO639P3code'].null = ['?']
        # args.writer.cldf['LanguageTable', 'Macroarea'].null = ['Eurasia']
        args.writer.cldf.add_columns('LanguageTable', 'Subfamily')
        args.writer.cldf.add_columns(
            'ValueTable',
            {
                'name': 'Example_ID',
                'separator': ' ',
                'propertyUrl': 'http://cldf.clld.org/v1.0/terms.rdf#exampleReference'})


    def cmd_makecldf(self, args):
        data = collections.defaultdict(dict)
        bibdata = database.parse_file(str(self.raw_dir.joinpath('sources.bib')))
        refs = collections.defaultdict(list)
        for key, entry in bibdata.entries.items():
            src = Source.from_entry(key, entry)
            for k in src:
                src[k] = unescape(src[k])
            for lid in src.get('langref', '').split(','):
                lid = lid.strip()
                refs[lid].append(src.id)
            args.writer.cldf.sources.add(src)

        for p in self.raw_dir.joinpath('UT', 'language-tables').glob('*.csv'):
            for row in reader(p, dicts=True):
                data[p.stem][row['ID']] = row

        examples = collections.defaultdict(list)
        for p in self.raw_dir.joinpath('UT', 'language-tables').glob('*_examples.csv'):
            for row in reader(p, dicts=True):
                if checkex(row):
                    examples[p.stem.replace('_examples', ''), row['ID']].append(row)

        self._schema(args)

        lmap = {}
        for lang in self.raw_dir.read_csv('Languages.csv', dicts=True):
            lang['ISO639P3code'] = lang.pop('ISO.639.3')
            lang['Source'] = refs.get(lang['Name'], [])
            del lang['citations']
            args.writer.objects['LanguageTable'].append(lang)
            lmap[lang['Name']] = lang['ID']
            lmap[lang['Glottocode']] = lang['ID']

        t = list(iter_markdown_tables(self.dir.joinpath('CONTRIBUTORS.md').read_text(encoding='utf8')))
        experts = collections.defaultdict(lambda: collections.defaultdict(list))
        for row in t[1][1]:
            row = list(zip(t[1][0], row))
            #[('ID', '33'), ('Subgroup', 'Mordvin'), ('Langauge', 'Moksha'), ('UT', '✔'), ('Language expert', 'Niina Aasmäe,  Mariann Bernhardt'), ('GB', '✔'), ('Language expert', 'Arja Hamari, Mariann Bernhardt')]
            contrib, lid = None, None
            for k, v in row:
                # "Langauge" (sic)
                if k == 'Langauge':
                    lid = lmap[unidecode(v).replace(' ', '_').replace('-', '_')]
                if k in ['UT', 'GB']:
                    contrib = k
                if k == 'Language expert':
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
        eid = 0
        for sd, contrib in [('UT', 'Uralic Areal Typology'), ('GB', 'Grambank')]:
            args.writer.objects['ContributionTable'].append(
                dict(ID=sd, Name=contrib))

            for param in read(self.raw_dir / sd / 'Features.csv'):
                param['Contribution_ID'] = sd
                doc = self.cldf_dir / '..' / 'doc' / '{}.md'.format(param['ID'])
                if doc.exists():
                    param['Feature_Description'] = str(doc.relative_to(self.cldf_dir))
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

            for row in read(self.raw_dir / sd / 'Finaldata.csv'):
                for k in row:
                    if k in ['language', 'subfam']:
                        continue
                    # if ('?' in row[k]) or ('!!' in row[k]):
                    #    continue
                    d = {}
                    lid = lmap[row['language']]
                    eids = []
                    if k.startswith('UT'):
                        d = data[row['language']][k]
                        #
                        # FIXME: change the way missing data is treated - at least for UT?
                        #
                        if row[k] in ['N/A']:  # don't even include the rows
                            continue
                        assert list(d.values())[2] == row[k], '{}, {}: {} != {}'.format(row['language'], k, list(d.values())[2], row[k])
                        if row[k] == '':
                            row[k] = '?'

                        for ex in examples.get((row['language'], k), []):
                            if ex['IPA']:
                                ex['Original_Script'] = ex['Primary_Text']
                                ex['Primary_Text'] = ex['IPA']

                            eid += 1
                            args.writer.objects['ExampleTable'].append(dict(
                                ID=str(eid),
                                Language_ID=lid,
                                Primary_Text=ex['Primary_Text'].strip().replace('-', ''),
                                Analyzed_Word=ex['Analyzed'].strip().split() if ex['Analyzed'] else [],
                                Gloss=ex['Gloss'].strip().split() if ex['Gloss'] else [],
                                Translated_Text=ex['Translation'].strip() or None,
                                Original_Script=ex.get('Original_Script', '').strip(),
                            ))
                            eids.append(str(eid))

                    args.writer.objects['ValueTable'].append(dict(
                        ID='{}-{}'.format(lid, k),
                        Language_ID=lid,
                        Parameter_ID=k,
                        Value='?' if row[k] in NA else str(int(float(row[k]))),
                        Code_ID=None if row[k] in NA else '{}-{}'.format(
                            k, int(float(row[k]))),
                        Comment=d.get('Comment'),
                        Example_ID=eids,
                    ))
