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
            HypervisorProperties.HYPERVISOR_ID: lambda a: a["id"],
            HypervisorProperties.HYPERVISOR_IP: lambda a: a["host_ip"],
            HypervisorProperties.HYPERVISOR_NAME: lambda a: a["name"],
            # HypervisorProperties.HYPERVISOR_SERVER_COUNT: lambda a: a["runnning_vms"],
            HypervisorProperties.HYPERVISOR_STATE: lambda a: a["state"],
            HypervisorProperties.HYPERVISOR_STATUS: lambda a: a["status"],
            HypervisorProperties.HYPERVISOR_DISABLED_REASON: lambda a: a["service"][
                "disabled_reason"
            ],
            HypervisorProperties.HYPERVISOR_UPTIME_DAYS: lambda a: TimeUtils.extract_uptime(
                a["uptime"]
            ),
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
