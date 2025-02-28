from unittest.mock import patch
import pytest

from openstackquery.enums.props.image_properties import ImageProperties
from openstackquery.exceptions.query_property_mapping_error import (
    QueryPropertyMappingError,
)

from tests.mocks.mocked_props import MockProperties


@pytest.mark.parametrize(
    "expected_prop,test_values",
    [
        (ImageProperties.IMAGE_CREATION_DATE, ["image_creation_date", "created_at"]),
        (
            ImageProperties.IMAGE_CREATION_PROGRESS,
            ["image_creation_progress", "progress"],
        ),
        (ImageProperties.IMAGE_ID, ["image_id", "id", "uuid"]),
        (
            ImageProperties.IMAGE_LAST_UPDATED_DATE,
            ["image_last_updated_date", "updated_at"],
        ),
        (ImageProperties.IMAGE_MINIMUM_RAM, ["image_minimum_ram", "min_ram", "ram"]),
        (
            ImageProperties.IMAGE_MINIMUM_DISK,
            ["image_minimum_disk", "min_disk", "disk"],
        ),
        (ImageProperties.IMAGE_NAME, ["image_name", "name"]),
        (ImageProperties.IMAGE_SIZE, ["image_size", "size"]),
        (ImageProperties.IMAGE_STATUS, ["image_status", "status"]),
    ],
)
def test_property_serialization(expected_prop, test_values, property_variant_generator):
    """Test all property name formats can be correctly serialized."""
    for variant in property_variant_generator(test_values):
        assert ImageProperties.from_string(variant) is expected_prop


@pytest.mark.parametrize("prop", list(ImageProperties))
def test_get_prop_mapping(prop):
    """
    Tests that all image properties have a property function mapping
    """
    ImageProperties.get_prop_mapping(prop)


def test_get_prop_mapping_invalid():
    """
    Tests that get_prop_mapping returns Error if property not supported
    """
    with pytest.raises(QueryPropertyMappingError):
        ImageProperties.get_prop_mapping(MockProperties.PROP_1)


@patch("openstackquery.enums.props.image_properties.ImageProperties.get_prop_mapping")
def test_get_marker_prop_func(mock_get_prop_mapping):
    """
    Tests that marker_prop_func returns get_prop_mapping called with IMAGE_ID
    """
    val = ImageProperties.get_marker_prop_func()
    mock_get_prop_mapping.assert_called_once_with(ImageProperties.IMAGE_ID)
    assert val == mock_get_prop_mapping.return_value
