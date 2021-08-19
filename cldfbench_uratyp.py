import pathlib

from clldutils.text import split_text

from cldfbench import Dataset as BaseDataset, CLDFSpec

GB_LANGUAGE_MAP = {
    #GB - UT
    #Central Mansi [cent2322]
    #Komi-Permyak [komi1269]
    #Ume Saami [umes1235]
    'gras1239': 'east2328',
    'kama1378': 'kama1351',
    'voro1241': 'sout2679',
    'west2392': 'kozy1238',
}


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

    def cmd_makecldf(self, args):
        args.writer.cldf.add_component('LanguageTable')
        args.writer.cldf.add_component('CodeTable')
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

        lmap = {}
        for lang in self.raw_dir.read_csv('Languages.csv', dicts=True):
            lang['ISO639P3code'] = lang.pop('ISO-639-3')
            args.writer.objects['LanguageTable'].append(lang)
            lmap[lang['Name']] = lang['ID']
            lmap[lang['Glottocode']] = lang['ID']

        args.writer.objects['ContributionTable'].append(dict(
            ID='UT', Name='Uralic Areal Typology'
        ))
        args.writer.objects['ContributionTable'].append(dict(
            ID='GB', Name='Grambank'
        ))

        for param in self.raw_dir.read_csv('Features.csv', dicts=True):
            param['Contribution_ID'] = 'UT'
            args.writer.objects['ParameterTable'].append(param)
            for code, name in [('1', 'yes'), ('0', 'no')]:
                args.writer.objects['CodeTable'].append(dict(
                    ID='{}-{}'.format(param['ID'], code),
                    Name=code,
                    Description=name,
                    Parameter_ID=param['ID'],
                ))
        gb_features = set()
        for row in self.raw_dir.read_csv('gb.csv', dicts=True):
            #Feature_ID,Feature,Possible Values
            gb_features.add(row['Feature_ID'])
            args.writer.objects['ParameterTable'].append(dict(
                ID=row['Feature_ID'],
                Name=row['Feature'],
                Contribution_ID='GB',
            ))
            try:
                for code, name in gb_codes(row['Possible Values']):
                    args.writer.objects['CodeTable'].append(dict(
                        ID='{}-{}'.format(row['Feature_ID'], code),
                        Name=code,
                        Description=name,
                        Parameter_ID=row['Feature_ID'],
                    ))
            except:
                print(row)
                raise
        for row in self.raw_dir.read_csv('Finaldata.csv', dicts=True):
            for k in row:
                lid = lmap[row['language']]
                if k.startswith('UT'):
                    if row[k] in ['', 'N/A']:  # don't even include the rows
                        continue
                    if '?' in row[k]:
                        continue
                    args.writer.objects['ValueTable'].append(dict(
                        ID='{}-{}'.format(lid, k),
                        Language_ID=lid,
                        Parameter_ID=k,
                        Value=row[k],
                        Code_ID='{}-{}'.format(k, row[k]),
                    ))
        seen = set()
        for sheet in self.raw_dir.glob('RK*.csv'):
            gc = sheet.stem.split('_')[-1].replace('.tsv', '')
            gc = GB_LANGUAGE_MAP.get(gc, gc)
            if gc in lmap and gc not in seen:
                seen.add(gc)
                for row in self.raw_dir.read_csv(sheet.name, dicts=True):
                    if row['Value'] and row['Feature_ID'] in gb_features:
                        args.writer.objects['ValueTable'].append(dict(
                            ID='{}-{}'.format(lmap[gc], row['Feature_ID']),
                            Language_ID=lmap[gc],
                            Parameter_ID=row['Feature_ID'],
                            Value=row['Value'],
                            Code_ID='{}-{}'.format(row['Feature_ID'], row['Value']) if row['Value'] != '?' else None,
                        ))
            else:
                print('skipping {}'.format(sheet))
