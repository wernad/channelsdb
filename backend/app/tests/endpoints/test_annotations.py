"""Tests for annotations endpoints."""

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.main import app

client = TestClient(app, base_url="http://testserver/api/v1")


@pytest.fixture(autouse=True)
def cleanup_dependencies():
    app.dependency_overrides = {}
    yield
    app.dependency_overrides = {}


@pytest.fixture
def mock_process_pdb_file():
    """Fixture for mocking process_pdb_file."""
    with patch("app.api.endpoints.annotations.process_pdb_file") as mock:
        mock.return_value = {"1abc": ({"1": {"dbResNum": "2"}})}
        yield mock


@pytest.fixture
def mock_fill_annotations_by_uniprot_id_pdb():
    """Fixture for mocking fill_annotations_by_uniprot_id."""
    with patch("app.api.endpoints.annotations.fill_annotations_by_uniprot_id") as mock:

        def mock_func(annotations, mapping, uniprot_id):
            annotations["entry_annotations"] = [{"uniprot_id": "1abc"}]

        mock.side_effect = mock_func
        yield mock


@pytest.fixture
def mock_fill_annotations_by_uniprot_id_uniprot():
    """Fixture for mocking fill_annotations_by_uniprot_id."""
    with patch("app.api.endpoints.annotations.fill_annotations_by_uniprot_id") as mock:

        def mock_func(annotations, mapping, uniprot_id):
            annotations["entry_annotations"] = [{"uniprot_id": "P12345"}]

        mock.side_effect = mock_func
        yield mock


def test_get_annotations_pdb_success(
    mock_process_pdb_file,
    mock_fill_annotations_by_uniprot_id_pdb,
):
    """Test successful retrieval of PDB annotations."""
    mock_id = "1abc"
    response = client.get(f"/annotations/{mock_id}")

    mock_fill_annotations_by_uniprot_id_pdb.assert_called_once()
    mock_process_pdb_file.assert_called_once()
    assert response.status_code == 200
    assert "EntryAnnotations" in response.json()
    assert response.json()["EntryAnnotations"] == [{"uniprot_id": "1abc"}]


def test_get_annotations_pdb_not_found(
    mock_process_pdb_file,
    mock_fill_annotations_by_uniprot_id_pdb,
):
    """Test retrieval of non-existent PDB annotations."""
    mock_process_pdb_file.side_effect = HTTPException(
        status_code=404, detail="Cannot find PDB ID '1abc'"
    )

    response = client.get("/annotations/1abc")

    assert response.status_code == 404
    assert "Cannot find PDB ID '1abc'" == response.json()["detail"]


def test_get_annotations_pdb_server_error(
    mock_process_pdb_file,
    mock_fill_annotations_by_uniprot_id_pdb,
):
    """Test retrieval when PDBe server returns an error."""
    mock_process_pdb_file.side_effect = HTTPException(
        status_code=503, detail="PDBe server returned an error"
    )

    response = client.get("/annotations/1abc")

    assert response.status_code == 503
    assert "PDBe server returned an error" == response.json()["detail"]


def test_get_annotations_uniprot_success(
    mock_fill_annotations_by_uniprot_id_uniprot,
):
    """Test successful retrieval of UniProt annotations."""
    response = client.get("/annotations/P12345")

    assert response.status_code == 200
    assert "EntryAnnotations" in response.json()
    assert response.json()["EntryAnnotations"] == [{"uniprot_id": "P12345"}]


def test_get_annotations_invalid_id():
    """Test retrieval with invalid ID format."""
    response = client.get("/annotations/invalid_id")

    assert response.status_code == 422
