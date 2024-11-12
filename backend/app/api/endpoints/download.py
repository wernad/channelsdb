from enum import StrEnum
from fastapi.responses import (
    FileResponse,
    RedirectResponse,
    PlainTextResponse,
    Response,
)


from fastapi import APIRouter

# from app.api.config import config
from app.api.common import (
    PDB_ID_Type,
    Uniprot_ID_Type,
    uniprot_id_404_response,
    pdb_id_404_response,
)
from app.api.dependencies import ExportServiceDep
from app.api.exceptions import ProteinNotFound, UnknownFileType

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
    export_service: ExportServiceDep,
    file_format: DownloadType,
    uniprot_id: Uniprot_ID_Type,
):
    return await download(export_service, file_format, uniprot_id)


@router.get(
    "/download/pdb/{pdb_id}/{file_format}",
    name="Download data",
    tags=["PDB"],
    description="Download various data about the protein",
    responses=pdb_id_404_response,
)
async def download_pdb(
    export_service: ExportServiceDep,
    file_format: DownloadType,
    pdb_id: PDB_ID_Type,
):
    return await download(export_service, file_format, pdb_id)


# TODO add output class
async def download(export_service: ExportServiceDep, file_format: DownloadType, structure_id: str):
    headers = {"Content-Disposition": f'attachment; filename="channelsdb_{structure_id}.{file_format.value}"'}

    # TODO handle png format later.
    match file_format:
        case DownloadType.json:
            result = export_service.get_json_file(structure_id)
            if not result:
                raise ProteinNotFound(protein_id=structure_id)

            return Response(
                content=result,
                media_type="application/json",
                headers=headers,
            )
        case DownloadType.pdb:
            result = export_service.get_pdb_file(structure_id)
        case DownloadType.pymol:
            result = export_service.get_pymol_file(structure_id)
        case DownloadType.chimera:
            result = export_service.get_chimera_file(structure_id)
        case DownloadType.vmd:
            result = export_service.get_vmd_file(structure_id)
        case DownloadType.zip:
            result = export_service.get_zip_file(structure_id)
            if not result:
                raise ProteinNotFound(protein_id=structure_id)
            return Response(
                content=result,
                media_type="application/zip",
                headers=headers,
            )
        case DownloadType.cif:
            file_path = "/home/chiro/Documen    ts/DP/channelsdb/backend/app/api/export/1tqn.cif"
            result = export_service.get_cif_file(file_path)
        case _:
            raise UnknownFileType(DownloadType.value)
    if not result:
        raise ProteinNotFound(protein_id=structure_id)

    return PlainTextResponse(result, headers=headers)
