import json
from argparse import ArgumentParser
from datetime import date
from collections import Counter
from zipfile import ZipFile
from pathlib import Path

from api import common


def get_statistics(datadir: str) -> dict[str, Counter]:
    counts = {}

    root = Path(datadir)
    for datafile in root.glob('**/data.zip'):
        pdb_id = datafile.parts[-2]
        counts[pdb_id] = Counter({value: 0 for value in common.TUNNEL_TYPES.values()})
        for file in ZipFile(datafile).namelist():
            name = Path(file).stem
            if name != 'annotations':
                counts[pdb_id][common.TUNNEL_TYPES[name]] += 1

    return counts


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('datadir', type=str, help='Directory with ChannelsDB data')
    parser.add_argument('statistics', type=str, help='Output statistics')
    parser.add_argument('content', type=str, help='Output summary contents')
    args = parser.parse_args()

    raw_stats = get_statistics(args.datadir)

    total = Counter()
    for partial in raw_stats.values():
        total += partial

    statistics = {
        'statistics': total,
        'date': date.today().strftime('%d/%m/%Y')
    }

    with open(args.statistics, 'w') as f:
        json.dump(statistics, f, sort_keys=True, indent=4)

    with open(args.content, 'w') as f:
        db_content = {}
        for pdb_id, counts in raw_stats.items():
            db_content[pdb_id] = [counts[value] for value in common.TUNNEL_TYPES.values()]
        json.dump(db_content, f, sort_keys=True)
