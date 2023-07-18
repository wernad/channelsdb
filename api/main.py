from enum import Enum
import gzip
import json
from pathlib import Path
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from zipfile import ZipFile
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

from api.config import config
from api.common import TUNNEL_TYPES
import api.externals

app = FastAPI(title='ChannelsDB API', contact={'name': 'Tomáš Raček', 'email': 'tomas.racek@ceitec.muni.cz'}, redoc_url=None, docs_url='/',
              version='beta', swagger_ui_parameters={'syntaxHighlight': False, 'defaultModelsExpandDepth': -1})


@app.get('/assembly/{pdb_id}', name='Assembly', tags=['Protein'], description='Returns prefered assembly for a given protein')
async def get_assembly_id(pdb_id: str):
    req = requests.get(f'https://www.ebi.ac.uk/pdbe/api/pdb/entry/summary/{pdb_id}')
    if req.status_code != 200:
        raise HTTPException(status_code=404, detail='Cannot find assembly for PDB ID \'{pdb_id}\'')
    data = json.loads(req.content)[pdb_id][0]['assemblies']
    return next(assembly['assembly_id'] for assembly in data if assembly['preferred'])


@app.get('/statistics', name='General statistics', tags=['General'], description='Returns summary statistics about the data stored')
async def get_statistics():
    with open(Path(config['dirs']['base']) / 'pdb_stats.json') as f:
        return json.load(f)


@app.get('/content', name='Database content', tags=['General'], description='Returns the counts of tunnels for each stored entry')
async def get_content():
    with open(Path(config['dirs']['base']) / 'db_content.json') as f:
        return json.load(f)


@app.get('/pdb/{pdb_id}', name='Channel data', tags=['Protein'], description='Returns information about channels for a given protein')
async def get_pdb_info(pdb_id: str):
    data = {'Annotations': [],
            'Channels': {TUNNEL_TYPES[name]: [] for name in TUNNEL_TYPES}}

    pdb_dir = Path(config['dirs']['data']) / pdb_id[1:3] / pdb_id

    if not Path(pdb_dir).exists():
        raise HTTPException(status_code=404, detail=f'PDB ID \'{pdb_id}\' not found in ChannelsDB')

    with ZipFile(pdb_dir / 'data.zip') as z:
        for json_file in z.namelist():
            if (name := Path(json_file).stem) in TUNNEL_TYPES:
                with z.open(json_file) as f:
                    # TODO We need to fix input data first
                    try:
                        orig = json.load(f)
                        res = []
                        for key in ('Paths', 'Tunnels', 'Pores', 'MergedPores'):
                            res.extend(orig['Channels'][key])
                        data['Channels'][TUNNEL_TYPES[name]] = res
                    except json.decoder.JSONDecodeError:
                        print(f'{pdb_id} / {json_file} not a correct JSON')
                        continue

        try:
            # TODO Do we need dummy annotations for channels not in annotations.json?
            with z.open('annotations.json') as f:
                data['Annotations'] = json.load(f)
        except KeyError:
            pass

    return data


@app.get('/annotations/{pdb_id}', name='Annotation data', tags=['Protein'],
         description='Returns annotations of individual protein and its residues')
async def get_annotations(pdb_id: str):
    annotations = {'EntryAnnotations': [],
                   'ResidueAnnotations': {
                       'ChannelsDB': [],
                       'UniProt': []
                   }}

    try:
        with urllib.request.urlopen(f'ftp://ftp.ebi.ac.uk/pub/databases/msd/sifts/xml/{pdb_id}.xml.gz') as f:
            xml_data = gzip.decompress(f.read()).decode('utf-8')
    except urllib.error.URLError:
        raise HTTPException(status_code=404, detail=f'Cannot find annotations for PDB ID \'{pdb_id}\'')

    sifts = api.externals.parse_sifts_data(xml_data)

    for uniprot_id, mapping in sifts.items():
        req = requests.get(f'https://www.ebi.ac.uk/proteins/api/proteins/{uniprot_id}', headers={'accept': 'application/xml'})
        xml_data = req.content.decode('utf-8')
        tree = ET.fromstring(xml_data)
        annotations['EntryAnnotations'].append(api.externals.get_entry_annotations(uniprot_id, tree))
        annotations['ResidueAnnotations']['UniProt'].extend(api.externals.get_uniprot_residue_annotations(mapping, tree))
        annotations['ResidueAnnotations']['ChannelsDB'].extend(api.externals.get_channelsdb_residue_annotations(uniprot_id, mapping))

    return annotations


class DownloadType(str, Enum):
    png = 'png'
    json = 'json'


@app.get('/download/{file_format}/{pdb_id}', name='Download data', tags=['Protein'], description='Download various data about the protein')
async def download(file_format: DownloadType, pdb_id: str):
    match file_format:
        case DownloadType.png:
            image_file = Path(config['dirs']['data']) / pdb_id[1:3] / pdb_id / f'{pdb_id}.png'

            if image_file.exists():
                return FileResponse(image_file)

            assembly_id = await get_assembly_id(pdb_id)

            return RedirectResponse(f'https://www.ebi.ac.uk/pdbe/static/entry/'
                                    f'{pdb_id}_assembly_{assembly_id}_chemically_distinct_molecules_front_image-200x200.png')
        case DownloadType.json:
            # TODO not implemented yet
            return 'NotImplementedYet'
