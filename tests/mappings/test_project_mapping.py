from openstackquery.enums.props.project_properties import ProjectProperties
from openstackquery.enums.props.server_properties import ServerProperties
from openstackquery.enums.query_presets import QueryPresets

from openstackquery.handlers.server_side_handler import ServerSideHandler
from openstackquery.mappings.project_mapping import ProjectMapping
from openstackquery.runners.project_runner import ProjectRunner


def test_get_runner_mapping():
    """
    Tests get runner mapping returns a flavor runner
    """
    assert ProjectMapping.get_runner_mapping() == ProjectRunner


def test_get_prop_mapping():
    """
    Tests get prop mapping returns a flavor properties
    """
    assert ProjectMapping.get_prop_mapping() == ProjectProperties


def test_get_server_side_handler_returns_correct_type():
    """
    Tests get server side handler returns a server side handler
    """
    assert isinstance(ProjectMapping.get_server_side_handler(), ServerSideHandler)


def test_server_side_handler_mappings_equal_to(server_side_test_mappings):
    """
    Tests server side handler mappings are correct, and line up to the expected
    server side params for equal to params
    """
    mappings = {
        ProjectProperties.PROJECT_ID: "id",
        ProjectProperties.PROJECT_DOMAIN_ID: "domain_id",
        ProjectProperties.PROJECT_IS_ENABLED: "is_enabled",
        ProjectProperties.PROJECT_IS_DOMAIN: "is_domain",
        ProjectProperties.PROJECT_NAME: "name",
        ProjectProperties.PROJECT_PARENT_ID: "parent_id",
    }

    server_side_test_mappings(
        ProjectMapping,
        QueryPresets.EQUAL_TO,
        mappings,
        test_case=(True, True),
    )


def test_server_side_handler_mappings_not_equal_to(server_side_test_mappings):
    """
    Tests server side handler mappings are correct, and line up to the expected
    server side params for equal to params
    """
    mappings = {
        ProjectProperties.PROJECT_IS_ENABLED: "is_enabled",
        ProjectProperties.PROJECT_IS_DOMAIN: "is_domain",
    }

    server_side_test_mappings(
        ProjectMapping,
        QueryPresets.NOT_EQUAL_TO,
        mappings,
        test_case=(True, False),
    )


def test_server_side_handler_mappings_any_in(server_side_any_in_mappings):
    """
    Tests server side handler mappings are correct for ANY_IN, and line up to the expected
    server side params for equal to params
    Tests that mappings render multiple server-side filters if multiple values given.
    Tests that equivalent equal to server-side filter exists for each ANY_IN filter - since they
    produce equivalent filters
    """

    mappings = {
        ProjectProperties.PROJECT_ID: "id",
        ProjectProperties.PROJECT_DOMAIN_ID: "domain_id",
        ProjectProperties.PROJECT_NAME: "name",
        ProjectProperties.PROJECT_PARENT_ID: "parent_id",
    }

    server_side_any_in_mappings(
        ProjectMapping,
        mappings,
        {"test1": "test1", "test2": "test2"},
    )


def test_client_side_handlers_generic(client_side_test_mappings):
    """
    Tests client side handler mappings are correct, and line up to the expected
    client side params for generic presets
    """
    handler = ProjectMapping.get_client_side_handler()
    mappings = {
        QueryPresets.EQUAL_TO: ["*"],
        QueryPresets.NOT_EQUAL_TO: ["*"],
        QueryPresets.ANY_IN: ["*"],
        QueryPresets.NOT_ANY_IN: ["*"],
    }
    client_side_test_mappings(handler, mappings)


def test_client_side_handlers_string(client_side_test_mappings):
    """
    Tests client side handler mappings are correct, and line up to the expected
    client side params for string presets
    """
    handler = ProjectMapping.get_client_side_handler()
    mappings = {
        QueryPresets.MATCHES_REGEX: [
            ProjectProperties.PROJECT_NAME,
            ProjectProperties.PROJECT_DESCRIPTION,
        ]
    }
    client_side_test_mappings(handler, mappings)


def test_get_chain_mappings():
    """
    Tests get_chain_mapping outputs correctly
    """
    expected_mappings = {ProjectProperties.PROJECT_ID: [ServerProperties.PROJECT_ID]}

    assert set(ProjectMapping.get_chain_mappings()) == set(expected_mappings)
