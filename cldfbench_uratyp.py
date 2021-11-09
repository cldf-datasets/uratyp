import re
import pathlib
import collections

from pybtex import database
from clld.lib.bibtex import unescape
from clldutils.text import split_text
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


def check_example(p, d):
    if d['Example']:
        ex = d['Example'].strip()
        ut_id = int(d["ID"].split('UT')[1])
        # ignore all the examples of phonological features in UT
        if 116 <= ut_id <= 166:
            pass
        else:
            if ex and ex.lower() != 'example':
                try:

                    # analyzed, gloss, translation = ex.split(
                    #     '\n' if '\n' in ex else ';')[:3]
                    analyzed, gloss, translation = re.split(r'\n|;', ex)[:3]
                    ipa = None
                    if '[' in analyzed:
                        analyzed, _, ipa = analyzed.partition('[')
                        analyzed = analyzed.strip()
                        ipa = ipa.replace(']', '').strip()
                    a = analyzed.strip().split()
                    g = gloss.strip().split()
                    if len(a) != len(g):
                        print('{}:{}:morphemes/gloss mismatch: "{}" - "{}"'.format(p.name,
                                                                                   d['ID'], ' '.join(a), ' '.join(g)))
                        # print(a)
                        # print(g)
                        # print('---')
                        #raise ValueError()
                except:
                    print('{}:{}:misformatted IGT: "{}"'.format(
                        p.name, d['ID'], ex.replace('\n', r'\n')))


NA = ['?', '0?', '1?', '?1', '!!', '?CHECK, possibly 0',
      '?CHECK, possibly 1', '?CHECK']


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "uratyp"

    def cldf_specs(self):  # A dataset must declare all CLDF sets it creates.
        return CLDFSpec(dir=self.cldf_dir, module="StructureDataset")

    def cmd_download(self, args):
        pass

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
                #
                # FIXME: check examples right here!
                #
                data[p.stem][row['ID']] = row
                check_example(p, row)
        args.writer.cldf.add_component(
            'LanguageTable',
            {
                'name': 'Source',
                'separator': ';',
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#source",
            })
        args.writer.cldf.add_component('CodeTable')
        args.writer.cldf.add_component(
            'ExampleTable',
            {
                'name': 'Analyzed_Word_IPA',
                'separator': '\t',
            }
        )
        t = args.writer.cldf.add_component('ContributionTable')
        t.common_props['dc:description'] = \
            "UraTyp combines typological data collected with two separate questionnaires. " \
            "These questionnaires are listed in the ContributionTable, and parameters, " \
            "i.e. features (and thus values) are linked to this table according to their origin."
        args.writer.cldf.add_component(
            'ParameterTable',
            'Area',
            {
                "name": "Contribution_ID",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#contributionReference",
                "dc:description": "Links a feature to the questionnaire it comes from.",
            },
        )
        args.writer.cldf['LanguageTable', 'Glottocode'].null = ['?']
        args.writer.cldf['LanguageTable', 'ISO639P3code'].null = ['?']
        # args.writer.cldf['LanguageTable', 'Macroarea'].null = ['Eurasia']
        args.writer.cldf.add_columns('LanguageTable', 'Subfamily')
        args.writer.cldf.add_columns(
            'ValueTable',
            {'name': 'Example_ID', 'propertyUrl': 'http://cldf.clld.org/v1.0/terms.rdf#exampleReference'})

        lmap = {}
        for lang in self.raw_dir.read_csv('Languages.csv', dicts=True):
            lang['ISO639P3code'] = lang.pop('ISO.639.3')
            lang['Source'] = refs.get(lang['Name'], [])
            del lang['citations']
            args.writer.objects['LanguageTable'].append(lang)
            lmap[lang['Name']] = lang['ID']
            lmap[lang['Glottocode']] = lang['ID']

        gb_features = {
            r['Feature_ID']: list(gb_codes(r['Possible Values']))
            for r in self.raw_dir.read_csv('gb.csv', dicts=True)}
        eid = 0
        for sd, contrib in [('UT', 'Uralic Areal Typology'), ('GB', 'Grambank')]:
            args.writer.objects['ContributionTable'].append(
                dict(ID=sd, Name=contrib))

            for param in read(self.raw_dir / sd / 'Features.csv'):
                param['Contribution_ID'] = sd
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
                    if k.startswith('UT'):
                        d = data[row['language']][k]
                        if row[k] in ['', 'N/A']:  # don't even include the rows
                            continue
                        assert list(d.values())[2] == row[k]
                        #assert row[k] != '1' or d['Example'], str(d)
                        if d['Example']:
                            ex = d['Example'].strip()
                            if ex and ex.lower() != 'example':
                                eid += 1
                                try:
                                    analyzed, gloss, translation = ex.split(
                                        '\n' if '\n' in ex else ';')[:3]
                                    ipa = None
                                    if '[' in analyzed:
                                        analyzed, _, ipa = analyzed.partition(
                                            '[')
                                        analyzed = analyzed.strip()
                                        ipa = ipa.replace(']', '').strip()
                                    a = analyzed.strip().split()
                                    g = gloss.strip().split()
                                    if len(a) != len(g):
                                        # print(a)
                                        # print(g)
                                        # print('---')
                                        raise ValueError()
                                    args.writer.objects['ExampleTable'].append(dict(
                                        ID=str(eid),
                                        Language_ID=lid,
                                        Primary_Text=analyzed.strip(),
                                        Analyzed_Word=a,
                                        Analyzed_Word_IPA=ipa.split() if ipa else [],
                                        Gloss=gloss.strip().split(),
                                        Translated_Text=translation.strip(),
                                    ))
                                except:
                                    args.writer.objects['ExampleTable'].append(dict(
                                        ID=str(eid),
                                        Language_ID=lid,
                                        Primary_Text=ex,
                                    ))

                    args.writer.objects['ValueTable'].append(dict(
                        ID='{}-{}'.format(lid, k),
                        Language_ID=lid,
                        Parameter_ID=k,
                        Value='?' if row[k] in NA else str(int(float(row[k]))),
                        Code_ID=None if row[k] in NA else '{}-{}'.format(
                            k, int(float(row[k]))),
                        Comment=d.get('Comment'),
                        Example_ID=str(eid) if d.get('Example') else None,
                    ))
