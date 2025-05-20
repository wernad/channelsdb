"""Tests for download endpoints."""

from app.database.models.source import Sources
from app.database.models.structure import StructureData
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.api.dependencies import get_structure_service, get_export_service
from app.main import app

client = TestClient(app, base_url="http://testserver/api/v1/download")


@pytest.fixture(autouse=True)
def cleanup_dependencies():
    app.dependency_overrides = {}
    yield
    app.dependency_overrides = {}


@pytest.fixture
def mock_structure_service():
    """Fixture for mocking structure service."""
    with patch("app.api.dependencies.get_structure_service") as mock:
        mock_service = Mock()
        mock.return_value = mock_service
        yield mock_service


@pytest.fixture
def mock_export_service():
    """Fixture for mocking export service."""
    with patch("app.api.dependencies.get_export_service") as mock:
        mock_service = Mock()
        mock.return_value = mock_service
        yield mock_service


@pytest.fixture
def mock_fetch_from_url():
    """Fixture for mocking fetch_from_url."""
    with patch("app.api.endpoints.download.fetch_from_url") as mock:
        mock.return_value = b"test_content"
        yield mock


@pytest.fixture
def mock_gzip_decompress():
    """Fixture for mocking gzip decompress."""
    with patch("app.api.endpoints.download.gzip.decompress") as mock:
        mock.return_value = b"test_content"
        yield mock


@pytest.fixture
def mock_get_file_url():
    """Fixture for mocking get_file_url."""
    with patch("app.api.endpoints.download.get_file_url") as mock:
        mock.return_value = "test_url"
        yield mock


def test_download_pdb_success(
    mock_structure_service,
    mock_export_service,
):
    """Test successful PDB file download."""
    structure_id = "1abc"
    internal_id = 123
    pdb_content = "ATOM      1  N   ALA A   1      27.526  24.362   4.697  1.00 20.00"
    mock_structure_service.get_newest_structure_with_channels_by_external_id.return_value = (
        internal_id
    )
    mock_export_service.get_pdb_file.return_value = pdb_content

    app.dependency_overrides[get_structure_service] = lambda: mock_structure_service
    app.dependency_overrides[get_export_service] = lambda: mock_export_service

    response = client.get(f"/{structure_id}?file_format=pdb")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    assert response.content.decode() == pdb_content


def test_download_cif_success(
    mock_structure_service,
    mock_export_service,
    mock_fetch_from_url,
    mock_gzip_decompress,
    mock_get_file_url,
):
    """Test successful CIF file download."""
    structure_id = "1abc"
    internal_id = 123
    cif_content = """data_1abc"""

    mock_structure_service.get_newest_structure_with_channels_by_external_id.return_value = (
        internal_id
    )
    mock_structure_service.get_source_and_version_by_external_id.return_value = (
        StructureData(
            source_id=Sources.PDB,
            version=1,
        )
    )
    mock_export_service.get_cif_file.return_value = cif_content
    mock_fetch_from_url.return_value = b"test_content"
    mock_gzip_decompress.return_value = "test_content"
    mock_get_file_url.return_value = "test_url"

    app.dependency_overrides[get_structure_service] = lambda: mock_structure_service
    app.dependency_overrides[get_export_service] = lambda: mock_export_service

    response = client.get(f"/{structure_id}?file_format=cif")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    assert response.content.decode() == cif_content


def test_download_chimera_success(
    mock_structure_service,
    mock_export_service,
):
    """Test successful Chimera visualization file download."""
    structure_id = "1abc"
    internal_id = 123
    chimera_content = """# Chimera visualization script
open 1abc.pdb
color bychain
surface transparency 0.5
"""

    mock_structure_service.get_newest_structure_with_channels_by_external_id.return_value = (
        internal_id
    )
    mock_export_service.get_chimera_file.return_value = chimera_content

    app.dependency_overrides[get_structure_service] = lambda: mock_structure_service
    app.dependency_overrides[get_export_service] = lambda: mock_export_service

    response = client.get(f"/{structure_id}?file_format=chimera")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    assert response.content.decode() == chimera_content


def test_download_pymol_success(
    mock_structure_service,
    mock_export_service,
):
    """Test successful PyMOL visualization file download."""
    structure_id = "1abc"
    internal_id = 123
    pymol_content = """# PyMOL visualization script
    load 1abc.pdb
    show surface
    color bychain
    """

    mock_structure_service.get_newest_structure_with_channels_by_external_id.return_value = (
        internal_id
    )
    mock_export_service.get_pymol_file.return_value = pymol_content

    app.dependency_overrides[get_structure_service] = lambda: mock_structure_service
    app.dependency_overrides[get_export_service] = lambda: mock_export_service

    response = client.get(f"/{structure_id}?file_format=pymol")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    assert response.content.decode() == pymol_content


def test_download_vmd_success(
    mock_structure_service,
    mock_export_service,
):
    """Test successful VMD visualization file download."""
    structure_id = "1abc"
    internal_id = 123
    vmd_content = """# VMD visualization script
    mol load pdb 1abc.pdb
    mol modstyle 0 0 NewCartoon
    mol modcolor 0 0 Chain
    """

    mock_structure_service.get_newest_structure_with_channels_by_external_id.return_value = (
        internal_id
    )
    mock_export_service.get_vmd_file.return_value = vmd_content

    app.dependency_overrides[get_structure_service] = lambda: mock_structure_service
    app.dependency_overrides[get_export_service] = lambda: mock_export_service

    response = client.get(f"/{structure_id}?file_format=vmd")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    assert response.content.decode() == vmd_content


def test_download_json_success(
    mock_structure_service,
    mock_export_service,
):
    """Test successful JSON file download."""
    structure_id = "1abc"
    internal_id = 123
    json_content = '{"channels": [{"id": 1, "name": "Channel1"}]}'

    mock_structure_service.get_newest_structure_with_channels_by_external_id.return_value = (
        internal_id
    )
    mock_export_service.get_json_file.return_value = json_content

    app.dependency_overrides[get_structure_service] = lambda: mock_structure_service
    app.dependency_overrides[get_export_service] = lambda: mock_export_service

    response = client.get(f"/{structure_id}?file_format=json")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"channels": [{"id": 1, "name": "Channel1"}]}


def test_download_no_channels(
    mock_structure_service,
    mock_export_service,
):
    """Test download when protein has no channels."""
    structure_id = "1abc"

    mock_structure_service.get_newest_structure_with_channels_by_external_id.return_value = (
        None
    )
    app.dependency_overrides[get_structure_service] = lambda: mock_structure_service
    app.dependency_overrides[get_export_service] = lambda: mock_export_service

    response = client.get(f"/{structure_id}?file_format=pdb")

    assert response.status_code == 404
    assert "has no channels" in response.json()["detail"]


def test_download_unknown_type(
    mock_structure_service,
    mock_export_service,
):
    """Test download with unknown file type."""
    structure_id = "1abc"
    internal_id = 123
    mock_structure_service.get_newest_structure_with_channels_by_external_id.return_value = (
        internal_id
    )
    app.dependency_overrides[get_structure_service] = lambda: mock_structure_service
    app.dependency_overrides[get_export_service] = lambda: mock_export_service

    response = client.get(f"/{structure_id}?file_format=unknown")

    assert response.status_code == 422
    assert isinstance(response.json()["detail"], list)


def test_download_invalid_id():
    """Test download with invalid structure ID."""
    response = client.get("/invalid_id/pdb")

    assert response.status_code == 404
    assert "Not Found" == response.json()["detail"]
