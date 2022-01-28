"""

"""
from csvw.dsv import reader, UnicodeWriter
from clldutils.clilib import PathType
from cldfbench_uratyp import Dataset


def register(parser):
    parser.add_argument('lang')


def parse(row):
    c = row['Example'].count(';')
    if c in [2, 3]:
        if c == 2:
            pt, gloss, translation = row['Example'].split(';')
            comment = ''
        else:
            pt, gloss, translation, comment = row['Example'].split(';')
        parsed = dict(Primary_Text=pt, Gloss=gloss, Translation=translation, Comment=comment)
        yield [parsed.get(k, row[k]) for k in row]
    else:
        yield [row[k] for k in row]


def split(row):
    for ex in row['Example'].split('|'):
        yield [row[k] if k != 'Example' else ex for k in row]


def run(args):
    ds = Dataset()
    for p in ds.raw_dir.joinpath('UT', 'language-tables').glob('*_examples.csv'):
        if args.lang in p.stem:
            rows = list(reader(p, dicts=True))
            with UnicodeWriter(p) as w:
                w.writerow(rows[0].keys())
                for row in rows:
                    w.writerows(list(split(row)))

        #    w.writerow(['ID', 'Example', 'Primary_Text', 'IPA', 'Analyzed', 'Gloss', 'Translation', 'Comment'])
        #    for row in rows:
        #        if row['Example'].strip().lower() not in ['examples', 'example', '']:
        #            w.writerow([row['ID'], row['Example'].strip(), '', '', '', '', '', ''])
