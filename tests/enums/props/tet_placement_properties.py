from unittest.mock import patch
import pytest

from openstackquery.enums.props.placement_properties import PlacementProperties
from openstackquery.exceptions.query_property_mapping_error import (
    QueryPropertyMappingError,
)

from tests.mocks.mocked_props import MockProperties


@pytest.mark.parametrize(
    "expected_prop,test_values",
    [
        (
            PlacementProperties.RESOURCE_PROVIDER_ID,
            ["resource_provider_id", "resource_provider_uuid", "id", "uuid"],
        ),
        (
            PlacementProperties.RESOURCE_PROVIDER_NAME,
            ["resource_provider_name", "name", "provider_name"],
        ),
        (PlacementProperties.VCPUS_AVAIL, ["vcpus_avail"]),
        (PlacementProperties.MEMORY_MB_AVAIL, ["memory_mb_avail"]),
        (PlacementProperties.DISK_GB_AVAIL, ["disk_gb_avail"]),
        (PlacementProperties.VCPUS_USED, ["vcpus_used"]),
        (PlacementProperties.MEMORY_MB_USED, ["memory_mb_used"]),
        (PlacementProperties.DISK_GB_USED, ["disk_gb_used"]),
    ],
)
def test_property_serialization(expected_prop, test_values, property_variant_generator):
    """Test all property name formats can be correctly serialized."""
    for variant in property_variant_generator(test_values):
        assert PlacementProperties.from_string(variant) is expected_prop


@pytest.mark.parametrize("prop", list(PlacementProperties))
def test_get_prop_mapping(prop):
    """
    Tests that all placement properties have a property function mapping
    """
    PlacementProperties.get_prop_mapping(prop)


def test_get_prop_mapping_invalid():
    """
    Tests that get_prop_mapping returns Error if property not supported
    """
    with pytest.raises(QueryPropertyMappingError):
        PlacementProperties.get_prop_mapping(MockProperties.PROP_1)


@patch(
    "openstackquery.enums.props.placement_properties.PlacementProperties.get_prop_mapping"
)
def test_get_marker_prop_func(mock_get_prop_mapping):
    """
    Tests that marker_prop_func returns get_prop_mapping called with RESOURCE_PROVIDER_ID
    """
    val = PlacementProperties.get_marker_prop_func()
    mock_get_prop_mapping.assert_called_once_with(
        PlacementProperties.RESOURCE_PROVIDER_ID
    )
    assert val == mock_get_prop_mapping.return_value
