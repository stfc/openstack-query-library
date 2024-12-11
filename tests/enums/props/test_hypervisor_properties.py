from unittest.mock import patch
import pytest

from openstackquery.enums.props.hypervisor_properties import HypervisorProperties
from openstackquery.exceptions.query_property_mapping_error import (
    QueryPropertyMappingError,
)

from tests.mocks.mocked_props import MockProperties


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


@pytest.mark.parametrize(
    "val",
    [
        "hypervisor_disk_free",
        "Hypervisor_Disk_Free",
        "HyPeRvIsOr_DiSk_FrEe",
        "local_disk_free",
        "free_disk_gb",
    ],
)
def test_hypervisor_disk_free_serialization(val):
    """
    Tests that variants of HYPERVISOR_DISK_FREE can be serialized
    """
    assert (
        HypervisorProperties.from_string(val)
        is HypervisorProperties.HYPERVISOR_DISK_FREE
    )


@pytest.mark.parametrize(
    "val",
    [
        "hypervisor_disk_size",
        "Hypervisor_Disk_Size",
        "HyPeRvIsOr_DiSk_SiZe",
        "local_disk_size",
        "local_gb",
    ],
)
def test_hypervisor_disk_size_serialization(val):
    """
    Tests that variants of HYPERVISOR_DISK_SIZE can be serialized
    """
    assert (
        HypervisorProperties.from_string(val)
        is HypervisorProperties.HYPERVISOR_DISK_SIZE
    )


@pytest.mark.parametrize(
    "val",
    [
        "hypervisor_disk_used",
        "Hypervisor_Disk_Used",
        "HyPeRvIsOr_DiSk_UsEd",
        "local_disk_used",
        "local_disk_used",
    ],
)
def test_hypervisor_disk_used_serialization(val):
    """
    Tests that variants of HYPERVISOR_DISK_USED can be serialized
    """
    assert (
        HypervisorProperties.from_string(val)
        is HypervisorProperties.HYPERVISOR_DISK_USED
    )


@pytest.mark.parametrize(
    "val",
    ["hypervisor_id", "Hypervisor_ID", "HyPeRvIsOr_Id", "id", "uuid", "host_id"],
)
def test_hypervisor_id_serialization(val):
    """
    Tests that variants of HYPERVISOR_ID can be serialized
    """
    assert HypervisorProperties.from_string(val) is HypervisorProperties.HYPERVISOR_ID


@pytest.mark.parametrize(
    "val",
    ["hypervisor_ip", "Hypervisor_IP", "HyPeRvIsOr_Ip", "ip", "host_ip"],
)
def test_hypervisor_ip_serialization(val):
    """
    Tests that variants of HYPERVISOR_IP can be serialized
    """
    assert HypervisorProperties.from_string(val) is HypervisorProperties.HYPERVISOR_IP


@pytest.mark.parametrize(
    "val",
    [
        "hypervisor_memory_free",
        "Hypervisor_Memory_Free",
        "HyPeRvIsOr_MeMoRy_FrEe",
        "memory_free",
        "free_ram_mb",
    ],
)
def test_hypervisor_memory_free_serialization(val):
    """
    Tests that variants of HYPERVISOR_MEMORY_FREE can be serialized
    """
    assert (
        HypervisorProperties.from_string(val)
        is HypervisorProperties.HYPERVISOR_MEMORY_FREE
    )


@pytest.mark.parametrize(
    "val",
    [
        "hypervisor_memory_size",
        "Hypervisor_Memory_Size",
        "HyPeRvIsOr_MeMoRy_SiZe",
        "memory_size",
        "memory_mb",
    ],
)
def test_hypervisor_memory_size_serialization(val):
    """
    Tests that variants of HYPERVISOR_MEMORY_SIZE can be serialized
    """
    assert (
        HypervisorProperties.from_string(val)
        is HypervisorProperties.HYPERVISOR_MEMORY_SIZE
    )


@pytest.mark.parametrize(
    "val",
    [
        "hypervisor_memory_used",
        "Hypervisor_Memory_Used",
        "HyPeRvIsOr_MeMoRy_UsEd",
        "memory_used",
        "memory_mb_used",
    ],
)
def test_hypervisor_memory_used_serialization(val):
    """
    Tests that variants of HYPERVISOR_MEMORY_USED can be serialized
    """
    assert (
        HypervisorProperties.from_string(val)
        is HypervisorProperties.HYPERVISOR_MEMORY_USED
    )


@pytest.mark.parametrize(
    "val",
    ["hypervisor_name", "Hypervisor_Name", "HyPeRvIsOr_NaMe", "name", "host_name"],
)
def test_hypervisor_name_serialization(val):
    """
    Tests that variants of HYPERVISOR_NAME can be serialized
    """
    assert HypervisorProperties.from_string(val) is HypervisorProperties.HYPERVISOR_NAME


@pytest.mark.parametrize(
    "val",
    [
        "hypervisor_state",
        "Hypervisor_State",
        "HyPeRvIsOr_StAtE",
        "state",
    ],
)
def test_hypervisor_state_serialization(val):
    """
    Tests that variants of HYPERVISOR_STATE can be serialized
    """
    assert (
        HypervisorProperties.from_string(val) is HypervisorProperties.HYPERVISOR_STATE
    )


@pytest.mark.parametrize(
    "val",
    [
        "hypervisor_status",
        "Hypervisor_Status",
        "HyPeRvIsOr_StAtuS",
        "status",
    ],
)
def test_hypervisor_status_serialization(val):
    """
    Tests that variants of HYPERVISOR_STATUS can be serialized
    """
    assert (
        HypervisorProperties.from_string(val) is HypervisorProperties.HYPERVISOR_STATUS
    )


@pytest.mark.parametrize(
    "val",
    [
        "hypervisor_vcpus",
        "Hypervisor_VCPUs",
        "HyPeRvIsOr_VcPuS",
        "vcpus",
    ],
)
def test_hypervisor_vcpus_serialization(val):
    """
    Tests that variants of HYPERVISOR_VCPUS can be serialized
    """
    assert (
        HypervisorProperties.from_string(val) is HypervisorProperties.HYPERVISOR_VCPUS
    )


@pytest.mark.parametrize(
    "val",
    [
        "hypervisor_vcpus_used",
        "Hypervisor_VCPUs_Used",
        "HyPeRvIsOr_VcPuS_uSeD",
        "vcpus_used",
    ],
)
def test_hypervisor_vcpus_used_serialization(val):
    """
    Tests that variants of HYPERVISOR_VCPUS_USED can be serialized
    """
    assert (
        HypervisorProperties.from_string(val)
        is HypervisorProperties.HYPERVISOR_VCPUS_USED
    )


@pytest.mark.parametrize(
    "val",
    [
        "hypervisor_disabled_reason",
        "Hypervisor_Disabled_Reason",
        "HyPeRvIsOr_DiSaBlEd_ReAsOn",
        "disabled_reason",
    ],
)
def test_hypervisor_disabled_reason_serialization(val):
    """
    Tests that variants of HYPERVISOR_DISABLED_REASON can be serialized
    """
    assert (
        HypervisorProperties.from_string(val)
        is HypervisorProperties.HYPERVISOR_DISABLED_REASON
    )


@pytest.mark.parametrize(
    "val",
    [
        "HYPERVISOR_UPTIME_DAYS",
        "Hypervisor_Uptime_Days",
        "HyPeRvIsOr_UpTiMe_DaYs",
    ],
)
def test_hypervisor_uptime_days_serialization(val):
    """
    Tests that variants of HYPERVISOR_UPTIME_DAYS can be serialized
    """
    assert (
        HypervisorProperties.from_string(val)
        is HypervisorProperties.HYPERVISOR_UPTIME_DAYS
    )
