from unittest.mock import patch

from openstackquery.enums.props.flavor_properties import FlavorProperties
from openstackquery.enums.props.hypervisor_properties import HypervisorProperties
from openstackquery.enums.props.image_properties import ImageProperties
from openstackquery.enums.props.project_properties import ProjectProperties
from openstackquery.enums.props.server_properties import ServerProperties
from openstackquery.enums.props.user_properties import UserProperties
from openstackquery.enums.query_presets import QueryPresets
from openstackquery.handlers.server_side_handler import ServerSideHandler
from openstackquery.mappings.server_mapping import ServerMapping
from openstackquery.runners.server_runner import ServerRunner


def test_get_runner_mapping():
    """
    Tests get runner mapping returns a server runner
    """
    assert ServerMapping.get_runner_mapping() == ServerRunner


def test_get_prop_mapping():
    """
    Tests get prop mapping returns a server properties
    """
    assert ServerMapping.get_prop_mapping() == ServerProperties


def test_get_server_side_handler_returns_correct_type():
    """
    Tests get server side handler returns a server side handler
    """
    assert isinstance(ServerMapping.get_server_side_handler(), ServerSideHandler)


def test_server_side_handler_mappings_equal_to(server_side_test_mappings):
    """
    Tests server side handler mappings are correct, and line up to the expected
    server side params for equal to params
    """
    mappings = {
        ServerProperties.USER_ID: "user_id",
        ServerProperties.SERVER_ID: "uuid",
        ServerProperties.SERVER_NAME: "hostname",
        ServerProperties.SERVER_STATUS: "status",
        ServerProperties.SERVER_DESCRIPTION: "description",
        ServerProperties.SERVER_CREATION_DATE: "created_at",
        ServerProperties.FLAVOR_ID: "flavor",
        ServerProperties.IMAGE_ID: "image",
        ServerProperties.PROJECT_ID: "project_id",
    }
    server_side_test_mappings(
        ServerMapping,
        QueryPresets.EQUAL_TO,
        mappings,
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
        ServerProperties.USER_ID: "user_id",
        ServerProperties.SERVER_ID: "uuid",
        ServerProperties.SERVER_NAME: "hostname",
        ServerProperties.SERVER_STATUS: "status",
        ServerProperties.SERVER_DESCRIPTION: "description",
        ServerProperties.SERVER_CREATION_DATE: "created_at",
        ServerProperties.FLAVOR_ID: "flavor",
        ServerProperties.IMAGE_ID: "image",
        ServerProperties.PROJECT_ID: "project_id",
    }
    server_side_any_in_mappings(
        ServerMapping,
        mappings,
        {"test1": "test1", "test2": "test2"},
    )


@patch("openstackquery.mappings.server_mapping.TimeUtils")
def test_server_side_handler_mappings_older_than_or_equal_to(
    mock_time_utils, server_side_test_mappings
):
    """
    Tests server side handler mappings are correct, and line up to the expected
    server side params for older_than_or_equal_to params
    """
    mock_time_utils.convert_to_timestamp.return_value = "test"
    mappings = {
        ServerProperties.SERVER_LAST_UPDATED_DATE: "changes-before",
    }
    server_side_test_mappings(
        ServerMapping,
        QueryPresets.OLDER_THAN_OR_EQUAL_TO,
        mappings,
    )

    # filter_func is evaluated twice, but convert_to_timestamp is only called once
    mock_time_utils.convert_to_timestamp.assert_called_once_with(value="test")


@patch("openstackquery.mappings.server_mapping.TimeUtils")
def test_server_side_handler_mappings_younger_than_or_equal_to(
    mock_time_utils, server_side_test_mappings
):
    """
    Tests server side handler mappings are correct, and line up to the expected
    server side params for younger_than_or_equal_to params
    """
    mock_time_utils.convert_to_timestamp.return_value = "test"
    mappings = {
        ServerProperties.SERVER_LAST_UPDATED_DATE: "changes-since",
    }
    server_side_test_mappings(
        ServerMapping,
        QueryPresets.YOUNGER_THAN_OR_EQUAL_TO,
        mappings,
    )

    # filter_func is evaluated twice, but convert_to_timestamp is only called once
    mock_time_utils.convert_to_timestamp.assert_called_once_with(value="test")


def test_client_side_handlers_generic(client_side_test_mappings):
    """
    Tests client side handler mappings are correct, and line up to the expected
    client side params for generic presets
    """
    handler = ServerMapping.get_client_side_handler()
    string_props = [
        ServerProperties.SERVER_NAME,
        ServerProperties.ADDRESSES,
    ]
    date_props = [
        ServerProperties.SERVER_LAST_UPDATED_DATE,
        ServerProperties.SERVER_CREATION_DATE,
    ]
    mappings = {
        QueryPresets.EQUAL_TO: ["*"],
        QueryPresets.NOT_EQUAL_TO: ["*"],
        QueryPresets.ANY_IN: ["*"],
        QueryPresets.NOT_ANY_IN: ["*"],
        QueryPresets.MATCHES_REGEX: string_props,
        QueryPresets.NOT_MATCHES_REGEX: string_props,
        QueryPresets.OLDER_THAN_OR_EQUAL_TO: date_props,
        QueryPresets.YOUNGER_THAN_OR_EQUAL_TO: date_props,
        QueryPresets.YOUNGER_THAN: date_props,
        QueryPresets.OLDER_THAN: date_props,
    }
    client_side_test_mappings(handler, mappings)


def test_get_chain_mappings():
    """
    Tests get_chain_mapping outputs correctly
    """
    expected_mappings = {
        ServerProperties.USER_ID: [UserProperties.USER_ID],
        ServerProperties.PROJECT_ID: [ProjectProperties.PROJECT_ID],
        ServerProperties.FLAVOR_ID: [FlavorProperties.FLAVOR_ID],
        ServerProperties.IMAGE_ID: [ImageProperties.IMAGE_ID],
        ServerProperties.HYPERVISOR_NAME: [
            HypervisorProperties.HYPERVISOR_NAME,
        ],
    }

    assert set(ServerMapping.get_chain_mappings()) == set(expected_mappings)
