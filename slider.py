import argparse

import pandas
from tabulate import tabulate


def main(args: argparse.Namespace) -> None:
    df = pandas.read_csv(args.data)

    df['week'] = df.index.map(lambda i: i+1)
    
    labels = df.columns.tolist()
    labels.insert(0, labels.pop())
    df = df[labels]
    
    df['diff'] = df.apply(lambda row: row.spent - row.total, axis=1)
    df['cum_diff'] = df['diff'].cumsum() # type: ignore
    
    with open(args.output, 'w') as out:
        output = tabulate(df,
                          tablefmt=args.format,
                          showindex='never',
                          headers='keys')
        out.write(output)
        print(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate extra work hours.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--data', default='data/data.csv', help='input file')
    parser.add_argument('-o', '--output', default='hours.md', help='output file')
    parser.add_argument('-f', '--format', default='github', help='output table format for tabulate [https://github.com/astanin/python-tabulate#table-format]')
    args = parser.parse_args()
    main(args)
