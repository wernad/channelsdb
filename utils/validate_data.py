import json
from argparse import ArgumentParser
from pathlib import Path
from zipfile import ZipFile


def validate(datadir: str):
    root = Path(datadir)
    for datafile in root.glob('Data/**/data.zip'):
        with ZipFile(datafile) as z:
            for file in z.namelist():
                with z.open(file) as f:
                    try:
                        json.load(f)
                    except json.decoder.JSONDecodeError:
                        print(f'{datafile}/{file} is not a valid JSON')
    for datafile in root.glob('Annotations/*.json'):
        with open(datafile) as f:
            try:
                json.load(f)
            except json.decoder.JSONDecodeError:
                print(f'{datafile}/ is not a valid JSON')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('datadir', type=str, help='irectory with ChannelsDB data')
    args = parser.parse_args()
    validate(args.datadir)
