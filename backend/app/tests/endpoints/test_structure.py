"""Tests for structure endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.api.dependencies import get_structure_service
from app.main import app

client = TestClient(app, base_url="http://testserver/api/v1")


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


def test_get_structures_filtered_success(
    mock_structure_service,
):
    """Test successful structure filtering."""
    expected_ids = ["1ABC", "2DEF"]
    mock_structure_service.get_structures_by_filter.return_value = expected_ids

    app.dependency_overrides[get_structure_service] = lambda: mock_structure_service

    min_distance = 10
    max_distance = 20
    min_radius = 1.0
    max_radius = 2.0
    min_bottleneck = 1.0

    response = client.get(
        f"/structures/filter?min_distance={min_distance}&max_distance={max_distance}&min_radius={min_radius}&max_radius={max_radius}&min_bottleneck={min_bottleneck}"
    )

    assert response.status_code == 200
    assert response.json() == expected_ids


def test_get_structures_filtered_no_results(
    mock_structure_service,
):
    """Test structure filtering with no results."""
    mock_structure_service.get_structures_by_filter.return_value = []

    app.dependency_overrides[get_structure_service] = lambda: mock_structure_service

    min_distance = 1000
    max_distance = 2000

    response = client.get(
        f"/structures/filter?min_distance={min_distance}&max_distance={max_distance}"
    )

    assert response.status_code == 404
    assert "No structures found" in response.json()["detail"]


def test_get_structures_filtered_invalid_params():
    """Test structure filtering with invalid parameters."""
    min_distance = "invalid"
    max_distance = 20

    response = client.get(
        f"/structures/filter?min_distance={min_distance}&max_distance={max_distance}"
    )

    assert response.status_code == 422


def test_get_structures_filtered_extra_params():
    """Test structure filtering with extra parameters."""
    min_distance = 10
    max_distance = 20
    extra_param = "extra"

    response = client.get(
        f"/structures/filter?min_distance={min_distance}&max_distance={max_distance}&{extra_param}=1"
    )

    assert response.status_code == 422
