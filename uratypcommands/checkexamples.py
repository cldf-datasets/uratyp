"""

"""
import collections

from csvw.dsv import reader
from cldfbench_uratyp import Dataset


def run(args):
    inv = 0
    i = collections.Counter()
    for p in Dataset().raw_dir.joinpath('UT', 'language-tables').glob('*_examples.csv'):
        if not p.stem.startswith('Erz'):
            continue
        for row in reader(p, dicts=True):
            if not row['Primary_Text']:
                print(p.stem, row['ID'], row['Example'])
                inv += 1
                continue
            if row['Analyzed'] and row['Gloss']:
                a = row['Analyzed'].strip().split()
                g = row['Gloss'].strip().split()
                if len(a) != len(g):
                    inv += 1
                    print(p.stem, row['ID'])
                    print(a)
                    print(g)
                    continue
            i.update([p.stem])
    for k, v in i.most_common():
        print(k, v)
    print(sum(i.values()))
    print(inv)
