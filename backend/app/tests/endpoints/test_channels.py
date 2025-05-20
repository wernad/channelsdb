"""Tests for channels endpoints."""

from app.database.models.channel import ChannelOutput, ChannelsResponse
from app.database.models.layer import LayerGeometry, LayerInfo, LayerProperties, Layers
from app.database.models.profile import ProfileOutput
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.api.dependencies import (
    get_structure_service,
    get_channel_service,
    get_annotation_service,
)
from app.main import app

from app.api.exceptions import NoChannelsInProtein, ProteinNotFound
from app.database.models import AnnotationOutput

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


@pytest.fixture
def mock_channel_service():
    """Fixture for mocking channel service."""
    with patch("app.api.dependencies.get_channel_service") as mock:
        mock_service = Mock()
        mock.return_value = mock_service
        yield mock_service


@pytest.fixture
def mock_annotation_service():
    """Fixture for mocking annotation service."""
    with patch("app.api.dependencies.get_annotation_service") as mock:
        mock_service = Mock()
        mock.return_value = mock_service
        yield mock_service


def test_get_channels_success(
    mock_structure_service,
    mock_channel_service,
    mock_annotation_service,
):
    """Test successful retrieval of channel data."""
    # Mock service responses
    structure_id = "1abc"
    internal_id = 123
    expected_channels = {
        "test_method": [
            ChannelOutput(
                id="1",
                type="test_type",
                cavity="test_cavity",
                auto=True,
                profile=[
                    ProfileOutput(
                        distance=2,
                        charge=3,
                        radius=4,
                        free_radius=5,
                        t_value=6,
                        coord_x=7,
                        coord_y=8,
                        coord_z=9,
                    )
                ],
                layers=Layers(
                    residue_flow=["test_residue_flow"],
                    het_residues=["test_het_residues"],
                    layers_info=[
                        LayerInfo(
                            layer_geometry=LayerGeometry(
                                radius=1,
                                free_radius=2,
                                start_distance=3,
                                end_distance=4,
                                local_minimum=True,
                                bottleneck=True,
                            ),
                            properties=LayerProperties(
                                charge=7,
                                hydrophobicity=8,
                                hydropathy=9,
                                polarity=10,
                                mutability=11,
                                hydrophilicity=12,
                                num_positives=13,
                                num_negatives=14,
                                num_hydrophobics=15,
                                num_hydrophilics=16,
                            ),
                            residues=["test_residues"],
                        )
                    ],
                ),
            )
        ]
    }
    expected_annotations = [
        AnnotationOutput(
            id="1",
            name="Channel1",
            description="Description1",
            reference="Reference1",
            reference_type="ReferenceType1",
        )
    ]

    mock_structure_service.get_newest_structure_with_channels_by_external_id.return_value = (
        internal_id
    )
    mock_channel_service.get_channels_with_by_structure_internal_id.return_value = (
        expected_channels
    )
    mock_annotation_service.get_annotations_by_structure.return_value = (
        expected_annotations
    )

    app.dependency_overrides[get_structure_service] = lambda: mock_structure_service
    app.dependency_overrides[get_channel_service] = lambda: mock_channel_service
    app.dependency_overrides[get_annotation_service] = lambda: mock_annotation_service

    response = client.get(f"/channels/{structure_id}")

    expected_response = ChannelsResponse(
        channels=expected_channels,
        annotations=expected_annotations,
    ).model_dump(by_alias=True)

    assert response.status_code == 200
    assert response.json() == expected_response


def test_get_channels_no_channels(
    mock_structure_service,
):
    """Test retrieval when protein has no channels."""
    mock_id = "1abc"
    mock_structure_service.get_newest_structure_with_channels_by_external_id.return_value = (
        None
    )

    app.dependency_overrides[get_structure_service] = lambda: mock_structure_service

    response = client.get(f"/channels/{mock_id}")

    assert response.status_code == 404
    assert "has no channels" in response.json()["detail"]


def test_get_channels_not_found(
    mock_structure_service,
    mock_channel_service,
):
    """Test retrieval when protein is not found."""
    mock_id = "1abc"
    mock_structure_service.get_newest_structure_with_channels_by_external_id.return_value = (
        123
    )
    mock_channel_service.get_channels_with_by_structure_internal_id.return_value = []

    app.dependency_overrides[get_structure_service] = lambda: mock_structure_service
    app.dependency_overrides[get_channel_service] = lambda: mock_channel_service

    response = client.get(f"/channels/{mock_id}")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_get_channels_invalid_id():
    """Test retrieval with invalid structure ID."""
    response = client.get("/channels/invalid_id")

    assert response.status_code == 422
