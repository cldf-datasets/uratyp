import pathlib

from cldfbench import Dataset as BaseDataset, CLDFSpec


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "uratyp"

    def cldf_specs(self):  # A dataset must declare all CLDF sets it creates.
        return CLDFSpec(dir=self.cldf_dir, module="StructureDataset")

    def cmd_download(self, args):
        pass

    def cmd_makecldf(self, args):
        args.writer.cldf.add_component('ParameterTable', 'Area')
        args.writer.cldf.add_component('LanguageTable')
        args.writer.cldf.add_component('CodeTable')
        args.writer.cldf['LanguageTable', 'Glottocode'].null = ['?']
        args.writer.cldf['LanguageTable', 'ISO639P3code'].null = ['?']
        args.writer.cldf.add_columns('LanguageTable', 'Subfamily')

        lmap = {}
        for lang in self.raw_dir.read_csv('Languages.csv', dicts=True):
            lang['ISO639P3code'] = lang.pop('ISO-639-3')
            args.writer.objects['LanguageTable'].append(lang)
            lmap[lang['Name']] = lang['ID']

        for param in self.raw_dir.read_csv('Features.csv', dicts=True):
            args.writer.objects['ParameterTable'].append(param)
            for code, name in [('1', 'yes'), ('0', 'no')]:
                args.writer.objects['CodeTable'].append(dict(
                    ID='{}-{}'.format(param['ID'], code),
                    Name=code,
                    Description=name,
                    Parameter_ID=param['ID'],
                ))

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
