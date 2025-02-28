from unittest.mock import patch
import pytest

from openstackquery.enums.props.server_properties import ServerProperties
from openstackquery.exceptions.parse_query_error import ParseQueryError
from openstackquery.exceptions.query_property_mapping_error import (
    QueryPropertyMappingError,
)

from tests.mocks.mocked_props import MockProperties


@pytest.mark.parametrize(
    "expected_prop,test_values",
    [
        (ServerProperties.FLAVOR_ID, ["flavor_id"]),
        (ServerProperties.HYPERVISOR_NAME, ["hypervisor_name", "hv_name"]),
        (ServerProperties.IMAGE_ID, ["image_id"]),
        (ServerProperties.PROJECT_ID, ["project_id"]),
        (ServerProperties.SERVER_CREATION_DATE, ["server_creation_date", "created_at"]),
        (ServerProperties.SERVER_DESCRIPTION, ["server_description", "description"]),
        (ServerProperties.SERVER_ID, ["server_id", "vm_id", "id", "uuid"]),
        (
            ServerProperties.SERVER_LAST_UPDATED_DATE,
            ["server_last_updated_date", "updated_at"],
        ),
        (ServerProperties.SERVER_NAME, ["server_name", "vm_name", "name"]),
        (ServerProperties.SERVER_STATUS, ["server_status", "status", "vm_status"]),
        (ServerProperties.USER_ID, ["user_id"]),
        (ServerProperties.ADDRESSES, ["addresses", "ips", "vm_ips", "server_ips"]),
    ],
)
def test_property_serialization(expected_prop, test_values, property_variant_generator):
    """Test all property name formats can be correctly serialized."""
    for variant in property_variant_generator(test_values):
        assert ServerProperties.from_string(variant) is expected_prop


@pytest.mark.parametrize("prop", list(ServerProperties))
def test_get_prop_mapping(prop):
    """
    Tests that all server properties have a property function mapping
    """
    ServerProperties.get_prop_mapping(prop)


def test_get_prop_mapping_invalid():
    """
    Tests that get_prop_mapping returns Error if property not supported
    """
    with pytest.raises(QueryPropertyMappingError):
        ServerProperties.get_prop_mapping(MockProperties.PROP_1)


@patch("openstackquery.enums.props.server_properties.ServerProperties.get_prop_mapping")
def test_get_marker_prop_func(mock_get_prop_mapping):
    """
    Tests that marker_prop_func returns get_prop_mapping called with SERVER_ID
    """
    val = ServerProperties.get_marker_prop_func()
    mock_get_prop_mapping.assert_called_once_with(ServerProperties.SERVER_ID)
    assert val == mock_get_prop_mapping.return_value


def test_invalid_serialization():
    """
    Tests that error is raised when passes invalid string to all preset classes
    """
    with pytest.raises(ParseQueryError):
        ServerProperties.from_string("some-invalid-string")


def test_get_ips_with_valid_data():
    """
    Tests that get_ips works expectedly
    should get comma-spaced ips for each network in addresses
    """
    # Create a sample object with addresses
    obj = {
        "addresses": {
            "network1": [{"addr": "192.168.1.1"}, {"addr": "192.168.1.2"}],
            "network2": [{"addr": "10.0.0.1"}],
        }
    }

    # Call the get_ips method
    result = ServerProperties.get_ips(obj)

    # Check if the result is as expected
    expected_result = "192.168.1.1, 192.168.1.2, 10.0.0.1"
    assert result == expected_result


def test_get_ips_with_empty_data():
    """
    Tests that get_pis works expectedly
    should return empty string if addresses is empty
    """
    # Test with an empty object
    obj = {"addresses": {}}
    result = ServerProperties.get_ips(obj)
    assert result == ""
