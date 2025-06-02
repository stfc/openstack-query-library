from openstackquery.enums.props.server_properties import ServerProperties
from openstackquery.enums.props.user_properties import UserProperties
from openstackquery.enums.query_presets import QueryPresets
from openstackquery.handlers.server_side_handler import ServerSideHandler
from openstackquery.mappings.user_mapping import UserMapping
from openstackquery.runners.user_runner import UserRunner


def test_get_runner_mapping():
    """
    Tests get runner mapping returns a user runner
    """
    assert UserMapping.get_runner_mapping() == UserRunner


def test_get_prop_mapping():
    """
    Tests get prop mapping returns a server properties
    """
    assert UserMapping.get_prop_mapping() == UserProperties


def test_get_server_side_handler_returns_correct_type():
    """
    Tests get server side handler returns a server side handler
    """
    assert isinstance(UserMapping.get_server_side_handler(), ServerSideHandler)


def test_server_side_handler_mappings_equal_to(server_side_test_mappings):
    """
    Tests server side handler mappings are correct, and line up to the expected
    server side params for equal to params
    """
    mappings = {
        UserProperties.USER_DOMAIN_ID: "domain_id",
        UserProperties.USER_NAME: "name",
        UserProperties.USER_ID: "id",
    }

    server_side_test_mappings(
        UserMapping,
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
        UserProperties.USER_DOMAIN_ID: "domain_id",
        UserProperties.USER_NAME: "name",
        UserProperties.USER_ID: "id",
    }

    server_side_any_in_mappings(
        UserMapping,
        mappings,
        {"test1": "test1", "test2": "test2"},
    )


def test_client_side_handlers_generic(client_side_test_mappings):
    """
    Tests client side handler mappings are correct, and line up to the expected
    client side params for generic presets
    """
    handler = UserMapping.get_client_side_handler()
    mappings = {
        QueryPresets.EQUAL_TO: ["*"],
        QueryPresets.NOT_EQUAL_TO: ["*"],
        QueryPresets.ANY_IN: ["*"],
        QueryPresets.NOT_ANY_IN: ["*"],
        QueryPresets.MATCHES_REGEX: [
            UserProperties.USER_EMAIL,
            UserProperties.USER_NAME,
        ],
        QueryPresets.NOT_MATCHES_REGEX: [
            UserProperties.USER_EMAIL,
            UserProperties.USER_NAME,
        ],
    }
    client_side_test_mappings(handler, mappings)


def test_get_chain_mappings():
    """
    Tests get_chain_mapping outputs correctly
    """
    expected_mappings = {
        UserProperties.USER_ID: [ServerProperties.USER_ID],
    }

    assert set(UserMapping.get_chain_mappings()) == set(expected_mappings)
