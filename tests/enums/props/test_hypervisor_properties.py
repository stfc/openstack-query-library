from unittest.mock import patch
import pytest

from openstackquery.enums.props.hypervisor_properties import HypervisorProperties
from openstackquery.exceptions.query_property_mapping_error import (
    QueryPropertyMappingError,
)

from tests.mocks.mocked_props import MockProperties


@pytest.mark.parametrize(
    "expected_prop,test_values",
    [
        (
            HypervisorProperties.HYPERVISOR_ID,
            ["hypervisor_id", "id", "uuid", "host_id"],
        ),
        (HypervisorProperties.HYPERVISOR_IP, ["hypervisor_ip", "ip", "host_ip"]),
        (
            HypervisorProperties.HYPERVISOR_NAME,
            ["hypervisor_name", "name", "host_name"],
        ),
        (HypervisorProperties.HYPERVISOR_STATE, ["hypervisor_state", "state"]),
        (HypervisorProperties.HYPERVISOR_STATUS, ["hypervisor_status", "status"]),
        (
            HypervisorProperties.HYPERVISOR_DISABLED_REASON,
            ["hypervisor_disabled_reason", "disabled_reason"],
        ),
        (HypervisorProperties.HYPERVISOR_UPTIME_DAYS, ["hypervisor_uptime_days"]),
        (HypervisorProperties.VCPUS_AVAIL, ["vcpus_avail"]),
        (
            HypervisorProperties.MEMORY_MB_AVAIL,
            ["memory_mb_avail", "memory_avail", "memory_free", "free_ram_mb"],
        ),
        (
            HypervisorProperties.DISK_GB_AVAIL,
            ["disk_gb_avail", "disk_avail", "local_disk_free", "free_disk_gb"],
        ),
        (HypervisorProperties.VCPUS_USED, ["vcpus_used"]),
        (HypervisorProperties.MEMORY_MB_USED, ["memory_mb_used", "memory_used"]),
        (
            HypervisorProperties.DISK_GB_USED,
            ["disk_gb_used", "disk_used", "local_disk_used", "local_gb_used"],
        ),
        (
            HypervisorProperties.DISK_GB_SIZE,
            ["disk_gb_size", "disk", "local_disk", "local_gb"],
        ),
        (
            HypervisorProperties.MEMORY_MB_SIZE,
            ["memory_mb_size", "memory_size", "memory_mb", "memory", "ram"],
        ),
        (HypervisorProperties.VCPUS, ["vcpus"]),
    ],
)
def test_property_serialization(expected_prop, test_values, property_variant_generator):
    """Test all property name formats can be correctly serialized."""
    for variant in property_variant_generator(test_values):
        assert HypervisorProperties.from_string(variant) is expected_prop


@pytest.mark.parametrize("prop", list(HypervisorProperties))
def test_get_prop_mapping(prop):
    """
    Tests that all hypervisor properties have a property function mapping
    """
    HypervisorProperties.get_prop_mapping(prop)


def test_get_prop_mapping_invalid():
    """
    Tests that get_prop_mapping returns Error if property not supported
    """
    with pytest.raises(QueryPropertyMappingError):
        HypervisorProperties.get_prop_mapping(MockProperties.PROP_1)


@patch(
    "openstackquery.enums.props.hypervisor_properties.HypervisorProperties.get_prop_mapping"
)
def test_get_marker_prop_func(mock_get_prop_mapping):
    """
    Tests that marker_prop_func returns get_prop_mapping called with HYPERVISOR_ID
    """
    val = HypervisorProperties.get_marker_prop_func()
    mock_get_prop_mapping.assert_called_once_with(HypervisorProperties.HYPERVISOR_ID)
    assert val == mock_get_prop_mapping.return_value
