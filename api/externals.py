import json
from pathlib import Path
import xml.etree.ElementTree as ET

from api.config import config


def parse_sifts_data(xml_data: str) -> dict[str, tuple[str, dict[str, str]]]:
    tree = ET.fromstring(xml_data)
    data = {}
    ns = {'': 'http://www.ebi.ac.uk/pdbe/docs/sifts/eFamily.xsd'}
    for entity in tree.iterfind('entity', ns):
        chain = entity.attrib['entityId']
        for segment in entity.iterfind('segment', ns):
            for residue in segment.find('listResidue', ns):
                if (uniprot_node := residue.find('./crossRefDb[@dbCoordSys="UniProt"]', ns)) is not None:
                    uniprot_id = uniprot_node.attrib['dbAccessionId']
                    uniprot_res_num = uniprot_node.attrib['dbResNum']
                    if (pdb_node := residue.find('./crossRefDb[@dbCoordSys="PDBresnum"]', ns)) is not None:
                        pdb_res_num = pdb_node.attrib['dbResNum']
                        if uniprot_id in data:
                            data[uniprot_id][1].update({uniprot_res_num: pdb_res_num})
                        else:
                            data[uniprot_id] = (chain, {uniprot_res_num: pdb_res_num})
    return data


def get_entry_annotations(uniprot_id: str, tree: ET) -> dict:
    ns = {'': 'http://uniprot.org/uniprot'}

    entry = {'UniProtId': uniprot_id,
             'Function': '',
             'Catalytics': [],
             'Name': ''
             }

    if (function := tree.find('comment[@type="function"]/text', ns)) is not None:
        entry['Function'] = function.text

    for name_type in ('recommendedName', 'alternativeName', 'submittedName'):
        if (node := tree.find(f'protein/{name_type}/fullName', ns)) is not None:
            entry['Name'] = node.text
            break

    for catalytics in tree.iterfind('comment[@type="catalytic activity"]/*/text', ns):
        entry['Catalytics'].append(catalytics.text)

    return entry


def get_uniprot_residue_annotations(mapping: tuple[str, dict[str, str]], tree: ET) -> list[dict]:
    ns = {'': 'http://uniprot.org/uniprot'}

    references: dict[str, tuple[str, str]] = {}
    for evidence in tree.iterfind('evidence', ns):
        key = evidence.attrib['key']
        if (reference := evidence.find('source/dbReference', ns)) is not None:
            ref_id, ref_type = reference.attrib['id'], reference.attrib['type']
            references[key] = (ref_id, ref_type)

    features = {}
    for feature_type in ('sequence variant', 'active site', 'binding site', 'mutagenesis site', 'site', 'metal ion-binding site'):
        features[feature_type] = tree.findall(f'feature[@type="{feature_type}"]', ns)

    residue_annotations = []

    for feature_type in features.keys():
        for item in features[feature_type]:
            residue_annotation = {
                'Id': '',
                'Chain': '',
                'Reference': '',
                'ReferenceType': '',
                'Text': ''
            }
            try:
                position = item.find('location/position', ns)
                residue_annotation['Id'] = mapping[1][position.attrib['position']]

                residue_annotation['Chain'] = mapping[0]

                if (evidence := item.attrib.get('evidence', None)) is not None:
                    # TODO What to do with multiple references to a site? Now, picking first.
                    evidence = evidence.split()[0]
                    residue_annotation['Reference'] = references[evidence][0]
                    residue_annotation['ReferenceType'] = references[evidence][1]

                if feature_type in ('sequence variant', 'mutagenesis site'):
                    residue_annotation[
                        'Text'] = f'{item.find("original", ns).text} &rarr; {item.find("variation", ns).text}: {item.attrib["description"]}'
                else:
                    residue_annotation['Text'] = f'{item.attrib["type"].title()}: {item.attrib["description"]}'

            except (AttributeError, KeyError):
                continue

            residue_annotations.append(residue_annotation)

    return residue_annotations


def get_channelsdb_residue_annotations(uniprot_id: str, mapping: tuple[str, dict[str, str]]) -> list[dict]:
    path = Path(config['dirs']['annotations']) / f'{uniprot_id}.json'
    if not path.exists():
        return []

    with open(path) as f:
        data = json.load(f)

    for annotation in data:
        annotation['Chain'] = mapping[0]
        annotation['Id'] = mapping[1].get(annotation['Id'], None)

    return data
