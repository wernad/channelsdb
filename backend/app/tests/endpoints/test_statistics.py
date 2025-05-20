"""Tests for statistics endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.api.dependencies import get_statistics_service, get_structure_service
from app.main import app


client = TestClient(app, base_url="http://testserver/api/v1")


@pytest.fixture(autouse=True)
def cleanup_dependencies():
    app.dependency_overrides = {}
    yield
    app.dependency_overrides = {}


@pytest.fixture
def mock_statistics_service():
    """Fixture for mocking statistics service."""
    with patch("app.api.dependencies.get_statistics_service") as mock:
        mock_service = Mock()
        mock.return_value = mock_service
        yield mock_service


@pytest.fixture
def mock_structure_service():
    """Fixture for mocking structure service."""
    with patch("app.api.dependencies.get_structure_service") as mock:
        mock_service = Mock()
        mock.return_value = mock_service
        yield mock_service


def test_get_channel_counts_per_method_success(
    mock_statistics_service,
):
    """Test successful retrieval of channel counts per method."""
    expected_stats = {
        "date": "2024-03-20",
        "entries_count": 30,
        "statistics": {"method1": 10, "method2": 20},
    }

    mock_statistics_service.get_channel_counts_per_method.return_value = expected_stats

    app.dependency_overrides[get_statistics_service] = lambda: mock_statistics_service

    response = client.get("/statistics/methods")

    assert response.status_code == 200
    assert response.json() == expected_stats


def test_get_channel_counts_per_method_empty(
    mock_statistics_service,
):
    """Test retrieval of channel counts when no data exists."""
    expected_stats = {
        "date": "2024-03-20",
        "entries_count": 0,
        "statistics": {},
    }
    mock_statistics_service.get_channel_counts_per_method.return_value = expected_stats

    app.dependency_overrides[get_statistics_service] = lambda: mock_statistics_service

    response = client.get("/statistics/methods")

    assert response.status_code == 200
    assert response.json() == expected_stats


def test_get_channel_counts_per_method_by_id_success(
    mock_statistics_service,
    mock_structure_service,
):
    """Test successful retrieval of channel counts per method for a specific structure."""
    structure_id = "1abc"
    internal_id = 123
    expected_stats = {
        "date": "2024-03-20",
        "entries_count": 15,
        "statistics": {"method1": 5, "method2": 10},
    }

    mock_structure_service.get_newest_structure_with_channels_by_external_id.return_value = (
        internal_id
    )
    mock_statistics_service.get_channel_counts_per_methods_by_id.return_value = (
        expected_stats
    )

    app.dependency_overrides[get_statistics_service] = lambda: mock_statistics_service
    app.dependency_overrides[get_structure_service] = lambda: mock_structure_service

    response = client.get(f"/statistics/methods/{structure_id}")
    assert response.status_code == 200
    assert response.json() == expected_stats


def test_get_channel_counts_per_method_by_id_no_channels(
    mock_statistics_service,
    mock_structure_service,
):
    """Test retrieval of channel counts for structure with no channels."""
    structure_id = "1abc"
    mock_structure_service.get_newest_structure_with_channels_by_external_id.return_value = (
        None
    )

    app.dependency_overrides[get_statistics_service] = lambda: mock_statistics_service
    app.dependency_overrides[get_structure_service] = lambda: mock_structure_service

    response = client.get(f"/statistics/methods/{structure_id}")

    assert response.status_code == 404
    assert "has no channels" in response.json()["detail"]


def test_get_length_stats_success(
    mock_statistics_service,
):
    """Test successful retrieval of channel length statistics."""
    expected_stats = {
        "statistics": {
            "avg": 15.5,
            "min": 5.0,
            "max": 25.0,
            "median": 15.0,
            "stdev": 5.0,
        }
    }
    mock_statistics_service.get_channel_length_stats.return_value = expected_stats[
        "statistics"
    ]

    app.dependency_overrides[get_statistics_service] = lambda: mock_statistics_service

    response = client.get("/statistics/length")

    assert response.status_code == 200
    assert response.json() == expected_stats


def test_get_length_stats_no_data(
    mock_statistics_service,
):
    """Test retrieval of length statistics when no data exists."""
    mock_statistics_service.get_channel_length_stats.return_value = {
        "avg": None,
        "min": None,
        "max": None,
        "median": None,
        "stdev": None,
    }

    app.dependency_overrides[get_statistics_service] = lambda: mock_statistics_service

    response = client.get("/statistics/length")

    assert response.status_code == 404
    assert "Not enough data" in response.json()["detail"]


def test_get_bottleneck_stats_success(
    mock_statistics_service,
):
    """Test successful retrieval of bottleneck statistics."""
    expected_stats = {
        "statistics": {
            "avg": 2.5,
            "min": 1.0,
            "max": 4.0,
            "median": 2.0,
            "stdev": 0.5,
        }
    }
    mock_statistics_service.get_channel_bottleneck_stats.return_value = expected_stats[
        "statistics"
    ]

    app.dependency_overrides[get_statistics_service] = lambda: mock_statistics_service

    response = client.get("/statistics/bottleneck")

    assert response.status_code == 200
    assert response.json() == expected_stats


def test_get_bottleneck_stats_no_data(
    mock_statistics_service,
):
    """Test retrieval of bottleneck statistics when no data exists."""
    mock_statistics_service.get_channel_bottleneck_stats.return_value = {
        "avg": None,
        "min": None,
        "max": None,
        "median": None,
        "stdev": None,
    }

    app.dependency_overrides[get_statistics_service] = lambda: mock_statistics_service

    response = client.get("/statistics/bottleneck")

    assert response.status_code == 404
    assert "Not enough data" in response.json()["detail"]


def test_get_top_types_success(
    mock_statistics_service,
):
    """Test successful retrieval of top channel types."""
    expected_stats = {
        "statistics": {
            "Tunnel": 50,
            "Pore": 30,
            "Channel": 20,
            "total": 100,
        }
    }
    mock_statistics_service.get_top_5_types_by_channel_count.return_value = (
        expected_stats["statistics"]
    )

    app.dependency_overrides[get_statistics_service] = lambda: mock_statistics_service

    response = client.get("/statistics/top_types")

    assert response.status_code == 200
    assert response.json() == expected_stats


def test_get_top_types_no_data(
    mock_statistics_service,
):
    """Test retrieval of top types when no data exists."""
    mock_statistics_service.get_top_5_types_by_channel_count.return_value = None

    app.dependency_overrides[get_statistics_service] = lambda: mock_statistics_service

    response = client.get("/statistics/top_types")

    assert response.status_code == 404
    assert "Not enough data" in response.json()["detail"]


def test_get_top_proteins_success(
    mock_statistics_service,
):
    """Test successful retrieval of top proteins."""
    expected_stats = {"statistics": {"1ABC": 5, "2DEF": 3, "3GHI": 2}}
    mock_statistics_service.get_top_5_proteins_by_channel_count.return_value = (
        expected_stats["statistics"]
    )

    app.dependency_overrides[get_statistics_service] = lambda: mock_statistics_service

    response = client.get("/statistics/top_proteins")

    assert response.status_code == 200
    assert response.json() == expected_stats


def test_get_top_proteins_no_data(
    mock_statistics_service,
):
    """Test retrieval of top proteins when no data exists."""
    mock_statistics_service.get_top_5_proteins_by_channel_count.return_value = {}

    app.dependency_overrides[get_statistics_service] = lambda: mock_statistics_service

    response = client.get("/statistics/top_proteins")

    assert response.status_code == 404
    assert "Not enough data to calculate statistics." in response.json()["detail"]


def test_get_top_residues_success(
    mock_statistics_service,
):
    """Test successful retrieval of top residues."""
    expected_stats = {
        "statistics": {
            "ALA": 100,
            "GLY": 80,
            "LEU": 60,
            "total": 240,
        }
    }
    mock_statistics_service.get_top_5_residues_by_channel_count.return_value = (
        expected_stats["statistics"]
    )

    app.dependency_overrides[get_statistics_service] = lambda: mock_statistics_service

    response = client.get("/statistics/top_residues")

    assert response.status_code == 200
    assert response.json() == expected_stats


def test_get_top_residues_no_data(
    mock_statistics_service,
):
    """Test retrieval of top residues when no data exists."""
    mock_statistics_service.get_top_5_residues_by_channel_count.return_value = None

    app.dependency_overrides[get_statistics_service] = lambda: mock_statistics_service

    response = client.get("/statistics/top_residues")

    assert response.status_code == 404
    assert "Not enough data" in response.json()["detail"]
