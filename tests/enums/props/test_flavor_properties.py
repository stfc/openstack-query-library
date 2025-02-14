from unittest.mock import patch
import pytest

from openstackquery.enums.props.flavor_properties import FlavorProperties
from openstackquery.exceptions.query_property_mapping_error import (
    QueryPropertyMappingError,
)
from tests.mocks.mocked_props import MockProperties


@pytest.mark.parametrize(
    "expected_prop,test_values",
    [
        (
            FlavorProperties.FLAVOR_DESCRIPTION,
            ["flavor_description", "description", "desc"],
        ),
        (FlavorProperties.FLAVOR_DISK, ["flavor_disk", "disk", "disk_size"]),
        (
            FlavorProperties.FLAVOR_EPHEMERAL,
            ["flavor_ephemeral", "ephemeral", "ephemeral_disk", "ephemeral_disk_size"],
        ),
        (FlavorProperties.FLAVOR_ID, ["flavor_id", "id", "uuid"]),
        (FlavorProperties.FLAVOR_IS_DISABLED, ["flavor_is_disabled", "is_disabled"]),
        (FlavorProperties.FLAVOR_IS_PUBLIC, ["flavor_is_public", "is_public"]),
        (FlavorProperties.FLAVOR_NAME, ["flavor_name", "name"]),
        (FlavorProperties.FLAVOR_RAM, ["flavor_ram", "ram", "ram_size"]),
        (FlavorProperties.FLAVOR_SWAP, ["flavor_swap"]),
        (FlavorProperties.FLAVOR_VCPU, ["flavor_vcpu", "vcpu", "vcpus"]),
    ],
)
def test_property_serialization(expected_prop, test_values, property_variant_generator):
    """Test all property name formats can be correctly serialized."""
    for variant in property_variant_generator(test_values):
        assert FlavorProperties.from_string(variant) is expected_prop


@pytest.mark.parametrize("prop", list(FlavorProperties))
def test_get_prop_mapping(prop):
    """
    Tests that all flavor properties have a property function mapping
    """
    FlavorProperties.get_prop_mapping(prop)


def test_get_prop_mapping_invalid():
    """
    Tests that get_prop_mapping returns Error if property not supported
    """
    with pytest.raises(QueryPropertyMappingError):
        FlavorProperties.get_prop_mapping(MockProperties.PROP_1)


@patch("openstackquery.enums.props.flavor_properties.FlavorProperties.get_prop_mapping")
def test_get_marker_prop_func(mock_get_prop_mapping):
    """
    Tests that marker_prop_func returns get_prop_mapping called with FLAVOR_ID
    """
    val = FlavorProperties.get_marker_prop_func()
    mock_get_prop_mapping.assert_called_once_with(FlavorProperties.FLAVOR_ID)
    assert val == mock_get_prop_mapping.return_value
