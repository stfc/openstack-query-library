from unittest.mock import patch

import pytest

from openstackquery.enums.props.aggregate_properties import AggregateProperties
from openstackquery.exceptions.query_property_mapping_error import (
    QueryPropertyMappingError,
)
from tests.mocks.mocked_props import MockProperties


@pytest.mark.parametrize(
    "expected_prop,test_values",
    [
        (
            AggregateProperties.AGGREGATE_CREATED_AT,
            ["aggregate_created_at", "created_at"],
        ),
        (AggregateProperties.AGGREGATE_DELETED, ["aggregate_deleted", "deleted"]),
        (
            AggregateProperties.AGGREGATE_DELETED_AT,
            ["aggregate_deleted_at", "deleted_at"],
        ),
        (
            AggregateProperties.AGGREGATE_GPUNUM,
            ["aggregate_gpunum", "metadata_gpunum", "gpunum"],
        ),
        (
            AggregateProperties.AGGREGATE_HOST_IPS,
            ["aggregate_host_ips", "hosts", "host_ips"],
        ),
        (
            AggregateProperties.AGGREGATE_LOCAL_STORAGE_TYPE,
            [
                "aggregate_local_storage_type",
                "metadata_local_storage_type",
                "local_storage_type",
            ],
        ),
        (AggregateProperties.AGGREGATE_METADATA, ["aggregate_metadata", "metadata"]),
        (
            AggregateProperties.AGGREGATE_HOSTTYPE,
            ["aggregate_hosttype", "metadata_hosttype", "hosttype"],
        ),
        (AggregateProperties.AGGREGATE_ID, ["aggregate_id", "id", "uuid"]),
        (
            AggregateProperties.AGGREGATE_UPDATED_AT,
            ["aggregate_updated_at", "updated_at"],
        ),
    ],
)
def test_property_serialization(expected_prop, test_values, property_variant_generator):
    """Test all property name formats can be correctly serialized."""
    for variant in property_variant_generator(test_values):
        assert AggregateProperties.from_string(variant) is expected_prop


@pytest.mark.parametrize("prop", list(AggregateProperties))
def test_get_prop_mapping(prop):
    """
    Tests that all image properties have a property function mapping
    """
    AggregateProperties.get_prop_mapping(prop)


def test_get_prop_mapping_invalid():
    """
    Tests that get_prop_mapping returns Error if property not supported
    """
    with pytest.raises(QueryPropertyMappingError):
        AggregateProperties.get_prop_mapping(MockProperties.PROP_1)


@patch(
    "openstackquery.enums.props.aggregate_properties.AggregateProperties.get_prop_mapping"
)
def test_get_marker_prop_func(mock_get_prop_mapping):
    """
    Tests that marker_prop_func returns get_prop_mapping called with AGGREGATE_ID
    """
    val = AggregateProperties.get_marker_prop_func()
    mock_get_prop_mapping.assert_called_once_with(AggregateProperties.AGGREGATE_ID)
    assert val == mock_get_prop_mapping.return_value
