from enum import StrEnum
from pathlib import Path
from fastapi.responses import (
    FileResponse,
    RedirectResponse,
    PlainTextResponse,
    Response,
)
import io
import json
import zipfile

from fastapi import APIRouter

# from app.api.config import config
from app.api.common import (
    PDB_ID_Type,
    Uniprot_ID_Type,
    uniprot_id_404_response,
    pdb_id_404_response,
)
from app.api.dependencies import ChannelServiceDep
import app.api.export as exp

router = APIRouter()


class DownloadType(StrEnum):
    png = "png"
    json = "json"
    pdb = "pdb"
    pymol = "pymol"
    chimera = "chimera"
    vmd = "vmd"
    zip = "zip"
    cif = "cif"


@router.get(
    "/download/alphafill/{uniprot_id}/{file_format}",
    name="Download data",
    tags=["AlphaFill"],
    description="Download various data about the protein",
    responses=uniprot_id_404_response,
)
async def download_alphafill(
    channels_service: ChannelServiceDep,
    file_format: DownloadType,
    uniprot_id: Uniprot_ID_Type,
):
    return await download(channels_service, file_format, uniprot_id)


@router.get(
    "/download/pdb/{pdb_id}/{file_format}",
    name="Download data",
    tags=["PDB"],
    description="Download various data about the protein",
    responses=pdb_id_404_response,
)
async def download_pdb(
    channels_service: ChannelServiceDep,
    file_format: DownloadType,
    pdb_id: PDB_ID_Type,
):
    return await download(channels_service, file_format, pdb_id)


# TODO add output class
async def download(channels_service: ChannelServiceDep, file_format: DownloadType, structure_id: str):
    channels = channels_service.get_channels_by_structure_json(structure_id)

    headers = {"Content-Disposition": f'attachment; filename="channelsdb_{structure_id}.{file_format.value}"'}

    match file_format:
        case DownloadType.json:
            return Response(
                content=json.dumps(channels),
                media_type="application/json",
                headers=headers,
            )
        case DownloadType.pdb:
            return PlainTextResponse(exp.get_PDB_file(channels), headers=headers)
        case DownloadType.pymol:
            return PlainTextResponse(exp.get_Pymol_file(channels), headers=headers)
        case DownloadType.chimera:
            return PlainTextResponse(exp.get_Chimera_file(channels), headers=headers)
        case DownloadType.vmd:
            return PlainTextResponse(exp.get_VMD_file(channels), headers=headers)
        case DownloadType.zip:
            content = io.BytesIO()
            zf = zipfile.ZipFile(content, mode="w")
            zf.writestr(f"{structure_id}_chimera.py", exp.get_Chimera_file(channels))
            zf.writestr(f"{structure_id}_pymol.py", exp.get_Pymol_file(channels))
            zf.writestr(f"{structure_id}_vmd.tk", exp.get_VMD_file(channels))
            zf.writestr(f"{structure_id}_report.json", json.dumps(channels))
            zf.writestr(f"{structure_id}_channels.pdb", exp.get_PDB_file(channels))
            zf.close()

            return Response(
                content=content.getvalue(),
                media_type="application/zip",
                headers=headers,
            )
        case DownloadType.cif:
            return PlainTextResponse(exp.get_cif())
        case _:
            return "Unknown download file type received."
