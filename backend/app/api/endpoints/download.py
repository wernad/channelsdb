import json
from enum import StrEnum
import aiohttp

from fastapi.responses import (
    PlainTextResponse,
    RedirectResponse,
    Response,
)
from fastapi import APIRouter, HTTPException

from app.api.dependencies import ExportServiceDep, IDCheckDep
from app.api.exceptions import ProteinNotFound, UnknownFileType
from app.config import (
    PDB_HTTP_FILE_URL,
    ALPHAFILL_HTTP_FILE_URL,
    PDB_HTTP_ASSEMBLY_URL,
    PDB_HTTP_IMAGE_URL,
)
from app.log import logger as log

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


def get_full_pdb_id(id: str):
    """Returns 12-character id of given 4-character id."""
    return f"pdb_0000{id.lower()}"


def is_pdb(id: str) -> bool:
    """Checks if id is in PDB format or not."""
    if len(id) == 4 or len(id) == 12:
        return True
    return False


def get_file_url(id: str, version: str = None) -> str:
    """Create PDB entry url based on id and version.

    Parameters:
        id: structure id
        version: version to fetch
    Returns:
        tuple of bytes and error code
    """
    log.debug(f"Creating url for file - {id=} {version=}.")

    if is_pdb(id):
        log.debug("Creating PDB entry url.")
        category = id[-3:-1]
        full_id = get_full_pdb_id(id) if len(id) == 4 else id
        file_name = f"{full_id}_xyz_v{version}.cif.gz"
        url = f"{PDB_HTTP_FILE_URL}{category}/{full_id}/{file_name}"
    else:
        log.debug("Creating Alphafill entry url.")
        full_id = id.upper()
        url = f"{ALPHAFILL_HTTP_FILE_URL}{full_id}"

    log.debug(f"Created file url: {url}")
    return url


async def get_assembly_id(pdb_id: str) -> str | None:
    """Helper method to retrieve assembly id corresponding to given PDB id."""
    log.debug(f"Fetching assembly for PDB id {pdb_id}.")
    url = f"{PDB_HTTP_ASSEMBLY_URL}{pdb_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                req = await response.json()
                log.debug(f"Assembly fetching for {pdb_id} done.")
                data = req[pdb_id][0]["assemblies"]
                return next(
                    (
                        assembly["assembly_id"]
                        for assembly in data
                        if assembly["preferred"]
                    ),
                    None,
                )
            else:
                raise HTTPException(
                    status_code=503,
                    detail=f"PDBe API returned an error when accessing: {req.url}",
                )


# TODO add fetch of pdb file
@router.get(
    "/{structure_id}",
    name="General statistics",
    description="Returns summary statistics about the data stored",
)
async def download(
    export_service: ExportServiceDep,
    file_format: DownloadType,
    structure_id: IDCheckDep,
):
    headers = {
        "Content-Disposition": f'attachment; filename="channelsdb_{structure_id}.{file_format.value}"'
    }

    # TODO Alphafill png ?
    match file_format:
        case DownloadType.png:
            fetch_url = PDB_HTTP_IMAGE_URL
            if len(structure_id) == 12:
                short_id = structure_id[-4:]
                assembly_id = await get_assembly_id(short_id)
                fetch_url = fetch_url.replace("|protein_id|", short_id).replace(
                    "|assembly_id|", assembly_id
                )
            elif len(structure_id) == 4:
                assembly_id = await get_assembly_id(structure_id)
                fetch_url = fetch_url.replace("|protein_id|", structure_id).replace(
                    "|assembly_id|", assembly_id
                )

            else:
                log.debug("Alphafill entry has no image.")
                return "No image entry for Alphafill."

            return RedirectResponse(fetch_url)

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
        # TODO
        case DownloadType.cif:

            file = None
            # file_path = f"/home/chiro/Documents/DP/channelsdb/backend/app/services/{structure_id}.cif"
            result = export_service.get_cif_file(structure_id, file)
        case _:
            raise UnknownFileType(DownloadType.value)

    if not result:
        raise ProteinNotFound(protein_id=structure_id)

    return PlainTextResponse(result, headers=headers)
