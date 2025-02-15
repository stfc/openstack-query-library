from enums.props.placement_properties import PlacementProperties
from openstackquery.enums.props.placement_properties import PlacementProperties
from openstackquery.enums.props.server_properties import ServerProperties
from openstackquery.enums.props.hypervisor_properties import HypervisorProperties
from openstackquery.enums.query_presets import (
    QueryPresetsGeneric,
    QueryPresetsString,
    QueryPresetsInteger,
)
from openstackquery.handlers.server_side_handler import ServerSideHandler
from openstackquery.mappings.placement_mapping import PlacementMapping
from openstackquery.runners.placement_runner import PlacementRunner


def test_get_runner_mapping():
    """
    Tests get runner mapping returns a hypervisor runner
    """
    assert PlacementMapping.get_runner_mapping() == PlacementRunner


def test_get_prop_mapping():
    """
    Tests get prop mapping returns a hypervisor properties
    """
    assert PlacementMapping.get_prop_mapping() == PlacementProperties


def test_get_server_side_handler_returns_correct_type():
    """
    Tests get server side handler returns a server side handler
    """
    assert isinstance(PlacementMapping.get_server_side_handler(), ServerSideHandler)


def test_server_side_handler_mappings_equal_to(server_side_test_mappings):
    """
    Tests server side handler mappings are correct, and line up to the expected
    server side params for equal to params
    """
    mappings = {
        PlacementProperties.RESOURCE_PROVIDER_ID: "id",
        PlacementProperties.RESOURCE_PROVIDER_NAME: "name",
    }
    server_side_test_mappings(
        PlacementMapping.get_server_side_handler(),
        PlacementMapping.get_client_side_handlers().generic_handler,
        QueryPresetsGeneric.EQUAL_TO,
        mappings,
    )


def test_client_side_handlers_generic(client_side_test_mappings):
    """
    Tests client side handler mappings are correct, and line up to the expected
    client side params for generic presets
    """
    handler = PlacementMapping.get_client_side_handlers().generic_handler
    mappings = {
        QueryPresetsGeneric.EQUAL_TO: ["*"],
        QueryPresetsGeneric.NOT_EQUAL_TO: ["*"],
        QueryPresetsGeneric.ANY_IN: ["*"],
        QueryPresetsGeneric.NOT_ANY_IN: ["*"],
    }
    client_side_test_mappings(handler, mappings)


def test_client_side_handlers_string(client_side_test_mappings):
    """
    Tests client side handler mappings are correct, and line up to the expected
    client side params for string presets
    """
    expected_mappings = [
        PlacementProperties.RESOURCE_PROVIDER_ID,
        PlacementProperties.RESOURCE_PROVIDER_NAME,
    ]

    handler = PlacementMapping.get_client_side_handlers().string_handler
    mappings = {QueryPresetsString.MATCHES_REGEX: expected_mappings}
    client_side_test_mappings(handler, mappings)


def test_client_side_handlers_integer(client_side_test_mappings):
    """
    Tests client side handler mappings are correct
    shouldn't create an integer handler because there are no integer related properties for Server
    """
    integer_prop_list = [
        PlacementProperties.VCPUS_AVAIL,
        PlacementProperties.MEMORY_MB_AVAIL,
        PlacementProperties.DISK_GB_AVAIL,
        PlacementProperties.VCPUS_USED,
        PlacementProperties.MEMORY_MB_USED,
        PlacementProperties.DISK_GB_USED,
    ]

    handler = PlacementMapping.get_client_side_handlers().integer_handler
    mappings = {
        QueryPresetsInteger.LESS_THAN: integer_prop_list,
        QueryPresetsInteger.GREATER_THAN: integer_prop_list,
        QueryPresetsInteger.GREATER_THAN_OR_EQUAL_TO: integer_prop_list,
        QueryPresetsInteger.LESS_THAN_OR_EQUAL_TO: integer_prop_list,
    }
    client_side_test_mappings(handler, mappings)


def test_client_side_handlers_datetime():
    """
    Tests client side handler mappings are correct, and line up to the expected
    shouldn't create a datetime handler because there are no datetime related properties for Hypervisor
    """
    handler = PlacementMapping.get_client_side_handlers().datetime_handler
    assert not handler


def test_get_chain_mappings():
    """
    Tests get_chain_mapping outputs correctly
    """
    expected_mappings = {
        PlacementProperties.RESOURCE_PROVIDER_NAME: [
            HypervisorProperties.HYPERVISOR_NAME,
            ServerProperties.HYPERVISOR_NAME,
        ],
    }
    # we don't care about order
    assert set(PlacementMapping.get_chain_mappings()) == set(expected_mappings)
