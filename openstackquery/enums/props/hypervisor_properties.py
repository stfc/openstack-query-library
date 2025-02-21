from enum import auto
from typing import Dict, Optional

from openstackquery.enums.props.prop_enum import PropEnum, PropFunc
from openstackquery.exceptions.query_property_mapping_error import (
    QueryPropertyMappingError,
)
from openstackquery.time_utils import TimeUtils


class HypervisorProperties(PropEnum):
    """
    An enum class for all hypervisor properties
    """

    HYPERVISOR_ID = auto()
    HYPERVISOR_IP = auto()
    HYPERVISOR_NAME = auto()
    HYPERVISOR_STATE = auto()
    HYPERVISOR_STATUS = auto()
    HYPERVISOR_DISABLED_REASON = auto()
    HYPERVISOR_UPTIME_DAYS = auto()
    VCPUS = auto()
    VCPUS_USED = auto()
    VCPUS_AVAIL = auto()
    MEMORY_MB_SIZE = auto()
    MEMORY_MB_USED = auto()
    MEMORY_MB_AVAIL = auto()
    DISK_GB_SIZE = auto()
    DISK_GB_USED = auto()
    DISK_GB_AVAIL = auto()

    @staticmethod
    def _get_aliases() -> Dict:
        """
        A method that returns all valid string alias mappings
        """
        return {
            HypervisorProperties.HYPERVISOR_ID: ["id", "uuid", "host_id"],
            HypervisorProperties.HYPERVISOR_IP: ["ip", "host_ip"],
            HypervisorProperties.HYPERVISOR_NAME: ["name", "host_name"],
            HypervisorProperties.HYPERVISOR_STATE: ["state"],
            HypervisorProperties.HYPERVISOR_STATUS: ["status"],
            HypervisorProperties.HYPERVISOR_DISABLED_REASON: ["disabled_reason"],
            HypervisorProperties.HYPERVISOR_UPTIME_DAYS: ["uptime"],
            HypervisorProperties.VCPUS: ["vcpus"],
            HypervisorProperties.VCPUS_USED: ["vcpus_used"],
            HypervisorProperties.VCPUS_AVAIL: ["vcpus_avail", "vcpus_free"],
            HypervisorProperties.MEMORY_MB_SIZE: [
                "memory_mb_size",
                "memory_size",
                "memory_mb",
                "memory",
                "ram",
            ],
            HypervisorProperties.MEMORY_MB_USED: ["memory_mb_used", "memory_used"],
            HypervisorProperties.MEMORY_MB_AVAIL: [
                "memory_mb_avail",
                "memory_avail",
                "memory_free",
                "free_ram_mb",
            ],
            HypervisorProperties.DISK_GB_SIZE: [
                "disk_gb_size",
                "disk",
                "local_disk",
                "local_gb",
            ],
            HypervisorProperties.DISK_GB_USED: [
                "disk_gb_used",
                "disk_used",
                "local_disk_used",
                "local_gb_used",
            ],
            HypervisorProperties.DISK_GB_AVAIL: [
                "disk_gb_avail",
                "disk_avail",
                "local_disk_free",
                "free_disk_gb",
            ],
        }

    @staticmethod
    def get_prop_mapping(prop) -> Optional[PropFunc]:
        """
        Method that returns the property function if function mapping exists for a given Hypervisor Enum
        how to get specified property from an openstacksdk Hypervisor object is documented here:
        https://docs.openstack.org/openstacksdk/latest/user/resources/compute/v2/hypervisor.html
        :param prop: A HypervisorProperty Enum for which a function may exist for
        """
        mapping = {
            HypervisorProperties.HYPERVISOR_ID: lambda a: a.hv["id"],
            HypervisorProperties.HYPERVISOR_IP: lambda a: a.hv["host_ip"],
            HypervisorProperties.HYPERVISOR_NAME: lambda a: a.hv["name"],
            # HypervisorProperties.HYPERVISOR_SERVER_COUNT: lambda a: a["runnning_vms"],
            HypervisorProperties.HYPERVISOR_STATE: lambda a: a.hv["state"],
            HypervisorProperties.HYPERVISOR_STATUS: lambda a: a.hv["status"],
            HypervisorProperties.HYPERVISOR_DISABLED_REASON: lambda a: a.hv["service"][
                "disabled_reason"
            ],
            HypervisorProperties.HYPERVISOR_UPTIME_DAYS: lambda a: TimeUtils.extract_uptime(
                a.hv["uptime"]
            ),
            HypervisorProperties.VCPUS: lambda a: a.usage.vcpus,
            HypervisorProperties.VCPUS_AVAIL: lambda a: a.usage.vcpu_avail,
            HypervisorProperties.MEMORY_MB_SIZE: lambda a: a.usage.memory_mb_size,
            HypervisorProperties.MEMORY_MB_AVAIL: lambda a: a.usage.memory_mb_avail,
            HypervisorProperties.DISK_GB_SIZE: lambda a: a.usage.disk_gb_size,
            HypervisorProperties.DISK_GB_AVAIL: lambda a: a.usage.disk_gb_avail,
            HypervisorProperties.VCPUS_USED: lambda a: a.usage.vcpu_used,
            HypervisorProperties.MEMORY_MB_USED: lambda a: a.usage.memory_mb_used,
            HypervisorProperties.DISK_GB_USED: lambda a: a.usage.disk_gb_used,
        }
        try:
            return mapping[prop]
        except KeyError as exp:
            raise QueryPropertyMappingError(
                f"Error: failed to get property mapping, property {prop.name} is not supported in HypervisorProperties"
            ) from exp

    @staticmethod
    def get_marker_prop_func():
        """
        A getter method to return marker property function for pagination
        """
        return HypervisorProperties.get_prop_mapping(HypervisorProperties.HYPERVISOR_ID)
