from unittest.mock import patch
import pytest

from openstackquery.enums.props.project_properties import ProjectProperties
from openstackquery.exceptions.query_property_mapping_error import (
    QueryPropertyMappingError,
)

from tests.mocks.mocked_props import MockProperties


@pytest.mark.parametrize(
    "expected_prop,test_values",
    [
        (
            ProjectProperties.PROJECT_DESCRIPTION,
            ["project_description", "description", "desc"],
        ),
        (ProjectProperties.PROJECT_DOMAIN_ID, ["project_domain_id", "domain_id"]),
        (ProjectProperties.PROJECT_ID, ["project_id", "id", "uuid"]),
        (ProjectProperties.PROJECT_IS_DOMAIN, ["project_is_domain", "is_domain"]),
        (
            ProjectProperties.PROJECT_IS_ENABLED,
            ["project_is_enabled", "is_enabled", "ram"],
        ),
        (ProjectProperties.PROJECT_NAME, ["project_name", "name"]),
        (ProjectProperties.PROJECT_PARENT_ID, ["project_parent_id", "parent_id"]),
    ],
)
def test_property_serialization(expected_prop, test_values, property_variant_generator):
    """Test all property name formats can be correctly serialized."""
    for variant in property_variant_generator(test_values):
        assert ProjectProperties.from_string(variant) is expected_prop


@pytest.mark.parametrize("prop", list(ProjectProperties))
def test_get_prop_mapping(prop):
    """
    Tests that all project properties have a property function mapping
    """
    ProjectProperties.get_prop_mapping(prop)


def test_get_prop_mapping_invalid():
    """
    Tests that get_prop_mapping returns Error if property not supported
    """
    with pytest.raises(QueryPropertyMappingError):
        ProjectProperties.get_prop_mapping(MockProperties.PROP_1)


@patch(
    "openstackquery.enums.props.project_properties.ProjectProperties.get_prop_mapping"
)
def test_get_marker_prop_func(mock_get_prop_mapping):
    """
    Tests that marker_prop_func returns get_prop_mapping called with FLAVOR_ID
    """
    val = ProjectProperties.get_marker_prop_func()
    mock_get_prop_mapping.assert_called_once_with(ProjectProperties.PROJECT_ID)
    assert val == mock_get_prop_mapping.return_value
