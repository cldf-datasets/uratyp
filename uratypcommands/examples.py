"""

"""
import re

from csvw.dsv import reader, UnicodeWriter
from clldutils.clilib import PathType
from cldfbench_uratyp import Dataset

WORD_PATTERN = re.compile("(?P<Primary_Text>[^[]+)\[(?P<IPA>[^]]+)]\s*('|’|‘)(?P<Translation>[^'’’]+)('|’|’)")
GLOSS_PATTERN = re.compile("(?P<Primary_Text>[^[]+)\[(?P<Analyzed>[^]]+)]\s*(?P<Gloss>[a-zA-Z.123]+)")


def register(parser):
    parser.add_argument('lang')
    parser.add_argument('action', default='split')


def parse(row):
    c = row['Example'].count(';')
    if c in [2, 3, 4]:
        print(c, row['Example'])
        ipa = ''
        if c == 2:
            pt, gloss, translation = row['Example'].split(';')
            comment = ''
        elif c == 3:
            pt, gloss, translation, comment = row['Example'].split(';')
        elif c == 4:
            pt, ipa, gloss, translation, comment = row['Example'].split(';')
            if ipa.startswith('['):
                ipa = ipa[1:].strip()
            if ipa.endswith(']'):
                ipa = ipa[:-1].strip()
        else:
            raise ValueError
        parsed = dict(
            Primary_Text=pt,
            IPA=ipa,
            Gloss='\t'.join(gloss.split()),
            Translation=translation,
            Comment=comment)
        parsed['Analyzed'] = '\t'.join((ipa or pt).split())
        yield [parsed.get(k, row[k]) for k in row]
    else:
        m = WORD_PATTERN.fullmatch(row['Example'])
        if m:
            parsed = m.groupdict()
            yield [parsed.get(k, row[k]) for k in row]
        else:
            m = GLOSS_PATTERN.fullmatch(row['Example'])
            if m:
                parsed = m.groupdict()
                yield [parsed.get(k, row[k]) for k in row]
            else:
                yield [row[k] for k in row]


def split(row):
    for ex in row['Example'].split('|'):
        yield [row[k] if k != 'Example' else ex for k in row]


def run(args):
    cols = "ID Example Primary_Text IPA Analyzed Gloss Translation Comment".split()
    ds = Dataset()
    if args.action == 'prep':
        for p in ds.raw_dir.joinpath('UT', 'language-tables').glob('*.csv'):
            if args.lang in p.stem:
                if '_examples' not in p.stem:
                    with UnicodeWriter(p.parent / '{}_examples.csv'.format(p.stem)) as w:
                        w.writerow(cols)
                        for row in reader(p, dicts=True):
                            if row['Example']:
                                w.writerow([row['ID'], row['Example']] + [''] * (len(cols) - 2))
        return

    for p in ds.raw_dir.joinpath('UT', 'language-tables').glob('*_examples.csv'):
        if args.lang in p.stem:
            rows = list(reader(p, dicts=True))
            with UnicodeWriter(p) as w:
                w.writerow(rows[0].keys())
                for row in rows:
                    w.writerows(list((split if args.action == 'split' else parse)(row)))

        #    w.writerow(['ID', 'Example', 'Primary_Text', 'IPA', 'Analyzed', 'Gloss', 'Translation', 'Comment'])
        #    for row in rows:
        #        if row['Example'].strip().lower() not in ['examples', 'example', '']:
        #            w.writerow([row['ID'], row['Example'].strip(), '', '', '', '', '', ''])
