from unittest.mock import patch
import pytest

from openstackquery.enums.props.user_properties import UserProperties
from openstackquery.exceptions.parse_query_error import ParseQueryError
from openstackquery.exceptions.query_property_mapping_error import (
    QueryPropertyMappingError,
)

from tests.mocks.mocked_props import MockProperties


@pytest.mark.parametrize(
    "expected_prop,test_values",
    [
        (UserProperties.USER_DOMAIN_ID, ["user_domain_id", "domain_id"]),
        (
            UserProperties.USER_EMAIL,
            [
                "user_email",
                "email",
                "email_addr",
                "email_address",
                "user_email_address",
            ],
        ),
        (UserProperties.USER_DESCRIPTION, ["user_description", "description"]),
        (UserProperties.USER_ID, ["user_id", "id", "uuid"]),
        (UserProperties.USER_NAME, ["user_name", "name", "username"]),
    ],
)
def test_property_serialization(expected_prop, test_values, property_variant_generator):
    """Test all property name formats can be correctly serialized."""
    for variant in property_variant_generator(test_values):
        assert UserProperties.from_string(variant) is expected_prop


@pytest.mark.parametrize("prop", list(UserProperties))
def test_get_prop_mapping(prop):
    """
    Tests that all user properties have a property function mapping
    """
    UserProperties.get_prop_mapping(prop)


def test_get_prop_mapping_invalid():
    """
    Tests that get_prop_mapping returns Error if property not supported
    """
    with pytest.raises(QueryPropertyMappingError):
        UserProperties.get_prop_mapping(MockProperties.PROP_1)


@patch("openstackquery.enums.props.user_properties.UserProperties.get_prop_mapping")
def test_get_marker_prop_func(mock_get_prop_mapping):
    """
    Tests that marker_prop_func returns get_prop_mapping called with USER_ID
    """
    val = UserProperties.get_marker_prop_func()
    mock_get_prop_mapping.assert_called_once_with(UserProperties.USER_ID)
    assert val == mock_get_prop_mapping.return_value


def test_invalid_serialization():
    """
    Tests that error is raised when passes invalid string to all preset classes
    """
    with pytest.raises(ParseQueryError):
        UserProperties.from_string("some-invalid-string")
