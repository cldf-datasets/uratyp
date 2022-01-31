"""

"""
from csvw.dsv import reader
from cldfbench_uratyp import Dataset


def run(args):
    for p in Dataset().raw_dir.joinpath('UT', 'language-tables').glob('*_examples.csv'):
        for row in reader(p, dicts=True):
            if not row['Primary_Text']:
                print(p.stem, row['ID'], row['Example'])
            if row['Analyzed'] and row['Gloss']:
                a = row['Analyzed'].strip().split()
                g = row['Gloss'].strip().split()
                if len(a) != len(g):
                    print(p.stem, row['ID'])
                    print(a)
                    print(g)
