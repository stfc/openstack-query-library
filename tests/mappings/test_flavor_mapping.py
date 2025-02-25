from openstackquery.enums.props.flavor_properties import FlavorProperties
from openstackquery.enums.props.server_properties import ServerProperties
from openstackquery.enums.query_presets import QueryPresets
from openstackquery.handlers.server_side_handler import ServerSideHandler
from openstackquery.mappings.flavor_mapping import FlavorMapping
from openstackquery.runners.flavor_runner import FlavorRunner


def test_get_runner_mapping():
    """
    Tests get runner mapping returns a flavor runner
    """
    assert FlavorMapping.get_runner_mapping() == FlavorRunner


def test_get_prop_mapping():
    """
    Tests get prop mapping returns a flavor properties
    """
    assert FlavorMapping.get_prop_mapping() == FlavorProperties


def test_get_server_side_handler_returns_correct_type():
    """
    Tests get server side handler returns a server side handler
    """
    assert isinstance(FlavorMapping.get_server_side_handler(), ServerSideHandler)


def test_server_side_handler_mappings(server_side_test_mappings):
    """
    Tests server side handler mappings are correct, and line up to the expected
    server side params for equal to params
    """
    mappings = {FlavorProperties.FLAVOR_IS_PUBLIC: "is_public"}
    server_side_test_mappings(
        FlavorMapping,
        QueryPresets.EQUAL_TO,
        mappings,
        test_case=(True, True),
    )


def test_server_side_handler_less_than_or_equal_to(server_side_test_mappings):
    """
    Tests server side handler mappings are correct, and line up to the expected
    server side params for less_than_or_equal_to params
    """
    mappings = {
        FlavorProperties.FLAVOR_DISK: "minDisk",
        FlavorProperties.FLAVOR_RAM: "minRam",
    }
    server_side_test_mappings(
        FlavorMapping,
        QueryPresets.LESS_THAN_OR_EQUAL_TO,
        mappings,
        (10, 10),
    )

    # with strings which can convert to ints
    server_side_test_mappings(
        FlavorMapping,
        QueryPresets.LESS_THAN_OR_EQUAL_TO,
        mappings,
        ("10", 10),
    )

    # with floats which can convert to ints
    server_side_test_mappings(
        FlavorMapping,
        QueryPresets.LESS_THAN_OR_EQUAL_TO,
        mappings,
        (10.0, 10),
    )


def test_server_side_handler_not_equal_to(server_side_test_mappings):
    """
    Tests server side handler mappings are correct, and line up to the expected
    server side params for not_equal_to params
    """
    mappings = {
        FlavorProperties.FLAVOR_IS_PUBLIC: "is_public",
    }
    server_side_test_mappings(
        FlavorMapping,
        QueryPresets.NOT_EQUAL_TO,
        mappings,
        (True, False),
    )


def test_client_side_handlers(client_side_test_mappings):
    """
    Tests client side handler mappings are correct, and line up to the expected
    client side params for generic presets
    """
    integer_prop_list = [
        FlavorProperties.FLAVOR_RAM,
        FlavorProperties.FLAVOR_DISK,
        FlavorProperties.FLAVOR_EPHEMERAL,
        FlavorProperties.FLAVOR_SWAP,
        FlavorProperties.FLAVOR_VCPU,
    ]
    handler = FlavorMapping.get_client_side_handler()
    mappings = {
        QueryPresets.LESS_THAN: integer_prop_list,
        QueryPresets.LESS_THAN_OR_EQUAL_TO: integer_prop_list,
        QueryPresets.GREATER_THAN: integer_prop_list,
        QueryPresets.GREATER_THAN_OR_EQUAL_TO: integer_prop_list,
        QueryPresets.MATCHES_REGEX: [FlavorProperties.FLAVOR_NAME],
        QueryPresets.EQUAL_TO: ["*"],
        QueryPresets.NOT_EQUAL_TO: ["*"],
        QueryPresets.ANY_IN: ["*"],
        QueryPresets.NOT_ANY_IN: ["*"],
    }
    client_side_test_mappings(handler, mappings)


def test_get_chain_mappings():
    """
    Tests get_chain_mapping outputs correctly
    """
    expected_mappings = {
        FlavorProperties.FLAVOR_ID: [ServerProperties.FLAVOR_ID],
    }

    assert set(FlavorMapping.get_chain_mappings()) == set(expected_mappings)
