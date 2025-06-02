from openstackquery.enums.props.hypervisor_properties import HypervisorProperties
from openstackquery.enums.props.server_properties import ServerProperties
from openstackquery.enums.query_presets import QueryPresets
from openstackquery.handlers.server_side_handler import ServerSideHandler
from openstackquery.mappings.hypervisor_mapping import HypervisorMapping
from openstackquery.runners.hypervisor_runner import HypervisorRunner


def test_get_runner_mapping():
    """
    Tests get runner mapping returns a hypervisor runner
    """
    assert HypervisorMapping.get_runner_mapping() == HypervisorRunner


def test_get_prop_mapping():
    """
    Tests get prop mapping returns a hypervisor properties
    """
    assert HypervisorMapping.get_prop_mapping() == HypervisorProperties


def test_get_server_side_handler_returns_correct_type():
    """
    Tests get server side handler returns a server side handler
    """
    assert isinstance(HypervisorMapping.get_server_side_handler(), ServerSideHandler)


def test_client_side_handlers(client_side_test_mappings):
    """
    Tests client side handler mappings are correct
    shouldn't create an integer handler because there are no integer related properties for Server
    """
    integer_prop_list = [
        HypervisorProperties.VCPUS_AVAIL,
        HypervisorProperties.MEMORY_MB_AVAIL,
        HypervisorProperties.DISK_GB_AVAIL,
        HypervisorProperties.VCPUS_USED,
        HypervisorProperties.MEMORY_MB_USED,
        HypervisorProperties.DISK_GB_USED,
        HypervisorProperties.VCPUS,
        HypervisorProperties.DISK_GB_SIZE,
        HypervisorProperties.MEMORY_MB_SIZE,
    ]
    string_prop_list = [
        HypervisorProperties.HYPERVISOR_IP,
        HypervisorProperties.HYPERVISOR_NAME,
        HypervisorProperties.HYPERVISOR_DISABLED_REASON,
    ]

    handler = HypervisorMapping.get_client_side_handler()
    mappings = {
        QueryPresets.LESS_THAN: integer_prop_list,
        QueryPresets.GREATER_THAN: integer_prop_list,
        QueryPresets.GREATER_THAN_OR_EQUAL_TO: integer_prop_list,
        QueryPresets.LESS_THAN_OR_EQUAL_TO: integer_prop_list,
        QueryPresets.MATCHES_REGEX: string_prop_list,
        QueryPresets.NOT_MATCHES_REGEX: string_prop_list,
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
        HypervisorProperties.HYPERVISOR_NAME: [
            ServerProperties.HYPERVISOR_NAME,
        ],
    }
    # we don't care about order
    assert set(HypervisorMapping.get_chain_mappings()) == set(expected_mappings)
