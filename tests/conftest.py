import random
from pathlib import Path

from api.config import config


def get_stored_pdbs(datadir: str) -> list[str]:
    root = Path(datadir)
    pdb_ids = []
    for datafile in root.glob('**/data.zip'):
        pdb_ids.append(datafile.parts[-2])

    return pdb_ids


stored_pdb_ids = get_stored_pdbs(config['dirs']['pdb'])


def pytest_addoption(parser):
    parser.addoption('--subset', action='store', default='all', type=str, choices=('all', 'random', 'first'))
    parser.addoption('--count', action='store', default=10, type=int)


def pytest_generate_tests(metafunc):
    if 'stored_pdbs' in metafunc.fixturenames:
        subset = metafunc.config.option.subset
        count = metafunc.config.option.count
        if subset == 'all':
            metafunc.parametrize('stored_pdbs', stored_pdb_ids)
        elif subset == 'random':
            metafunc.parametrize('stored_pdbs', random.sample(stored_pdb_ids, k=count))
        else:
            # first
            metafunc.parametrize('stored_pdbs', stored_pdb_ids[:count])
