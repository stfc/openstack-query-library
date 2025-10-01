from dataclasses import dataclass
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
        (
            HypervisorProperties.VCPUS_AVAIL,
            [
                "vcpus_avail",
                "vcpus_free",
                "cpus_avail",
                "cpus_free",
                "pcpus_avail",
                "pcpus_free",
            ],
        ),
        (
            HypervisorProperties.MEMORY_MB_AVAIL,
            ["memory_mb_avail", "memory_avail", "memory_free", "free_ram_mb"],
        ),
        (
            HypervisorProperties.DISK_GB_AVAIL,
            ["disk_gb_avail", "disk_avail", "local_disk_free", "free_disk_gb"],
        ),
        (
            HypervisorProperties.VCPUS_USED,
            [
                "vcpus_used",
                "vcpus_in_use",
                "cpus_used",
                "cpus_in_use",
                "pcpus_used",
                "pcpus_in_use",
            ],
        ),
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
        (HypervisorProperties.VCPUS, ["vcpus", "cpus", "pcpus"]),
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


# pylint: disable=too-many-instance-attributes
@dataclass
class MockUsage:
    vcpus: int = 0
    pcpus: int = 0
    vcpus_used: int = 0
    pcpus_used: int = 0
    vcpus_avail: int = 0
    pcpus_avail: int = 0
    memory_mb_size: int = 0
    memory_mb_used: int = 0
    memory_mb_avail: int = 0
    disk_gb_size: int = 0
    disk_gb_used: int = 0
    disk_gb_avail: int = 0


@dataclass
class MockHypervisor:
    hv: dict
    usage: MockUsage


@pytest.mark.parametrize(
    "prop, mock_hv, mock_usage, expected",
    [
        (HypervisorProperties.HYPERVISOR_ID, {"id": "abc123"}, None, "abc123"),
        (HypervisorProperties.HYPERVISOR_IP, {"host_ip": "10.0.0.1"}, None, "10.0.0.1"),
        (HypervisorProperties.HYPERVISOR_NAME, {"name": "hyp1"}, None, "hyp1"),
        (HypervisorProperties.HYPERVISOR_STATE, {"state": "up"}, None, "up"),
        (
            HypervisorProperties.HYPERVISOR_STATUS,
            {"status": "enabled"},
            None,
            "enabled",
        ),
        (
            HypervisorProperties.HYPERVISOR_DISABLED_REASON,
            {"service": {"disabled_reason": "maintenance"}},
            None,
            "maintenance",
        ),
        (
            HypervisorProperties.VCPUS,
            {},
            MockUsage(vcpus=4, pcpus=2),
            6,
        ),
        (
            HypervisorProperties.VCPUS_USED,
            {},
            MockUsage(vcpus_used=1, pcpus_used=2),
            3,
        ),
        (
            HypervisorProperties.VCPUS_AVAIL,
            {},
            MockUsage(vcpus_avail=3, pcpus_avail=1),
            4,
        ),
        (
            HypervisorProperties.MEMORY_MB_SIZE,
            {},
            MockUsage(memory_mb_size=8192),
            8192,
        ),
        (
            HypervisorProperties.MEMORY_MB_USED,
            {},
            MockUsage(memory_mb_used=4096),
            4096,
        ),
        (
            HypervisorProperties.MEMORY_MB_AVAIL,
            {},
            MockUsage(memory_mb_avail=2048),
            2048,
        ),
        (
            HypervisorProperties.DISK_GB_SIZE,
            {},
            MockUsage(disk_gb_size=500),
            500,
        ),
        (
            HypervisorProperties.DISK_GB_USED,
            {},
            MockUsage(disk_gb_used=200),
            200,
        ),
        (
            HypervisorProperties.DISK_GB_AVAIL,
            {},
            MockUsage(disk_gb_avail=300),
            300,
        ),
    ],
)
def test_hypervisor_property_mappings(prop, mock_hv, mock_usage, expected):
    """Test that each HypervisorProperties mapping correctly extracts the expected data."""
    hv_obj = MockHypervisor(mock_hv, mock_usage)
    func = HypervisorProperties.get_prop_mapping(prop)
    assert func(hv_obj) == expected


@patch("openstackquery.enums.props.hypervisor_properties.TimeUtils.extract_uptime")
def test_hypervisor_uptime_days_mapping(mock_extract):
    mock_extract.return_value = 5
    hv_obj = MockHypervisor({"uptime": "fake-uptime-string"}, None)

    func = HypervisorProperties.get_prop_mapping(
        HypervisorProperties.HYPERVISOR_UPTIME_DAYS
    )
    result = func(hv_obj)

    mock_extract.assert_called_once_with("fake-uptime-string")
    assert result == 5
