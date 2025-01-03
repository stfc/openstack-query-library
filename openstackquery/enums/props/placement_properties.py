from enum import auto
from typing import Dict, Optional

from openstackquery.enums.props.prop_enum import PropEnum, PropFunc
from openstackquery.exceptions.query_property_mapping_error import (
    QueryPropertyMappingError,
)


class PlacementProperties(PropEnum):
    """
    An enum class for currently used placement properties
    """

    RESOURCE_PROVIDER_ID = auto()
    RESOURCE_PROVIDER_NAME = auto()
    VCPUS_USED = auto()
    VCPUS_AVAIL = auto()
    MEMORY_MB_USED = auto()
    MEMORY_MB_AVAIL = auto()
    DISK_GB_USED = auto()
    DISK_GB_AVAIL = auto()

    @staticmethod
    def _get_aliases() -> Dict:
        """
        A method that returns all valid string alias mappings
        """
        return {
            PlacementProperties.RESOURCE_PROVIDER_ID: [
                "resource_provider_id",
                "resource_provider_uuid",
                "id",
            ],
            PlacementProperties.RESOURCE_PROVIDER_NAME: [
                "resource_name",
                "name",
                "provider_name",
            ],
            PlacementProperties.VCPUS_USED: ["vcpus_used"],
            PlacementProperties.VCPUS_AVAIL: ["vcpus_avail"],
            PlacementProperties.MEMORY_MB_USED: ["memory_mb_used"],
            PlacementProperties.MEMORY_MB_AVAIL: ["memory_mb_avail"],
            PlacementProperties.DISK_GB_USED: ["disk_gb_used"],
            PlacementProperties.DISK_GB_AVAIL: ["disk_gb_avail"],
        }

    @staticmethod
    def get_prop_mapping(prop) -> Optional[PropFunc]:
        """
        Method that returns the property function if function mapping exists for a given Hypervisor Enum
        how to get specified property from a ResourceProviderUsage object
        :param prop: A HypervisorProperty Enum for which a function may exist for
        """
        mapping = {
            PlacementProperties.RESOURCE_PROVIDER_ID: lambda a: a["id"],
            PlacementProperties.RESOURCE_PROVIDER_NAME: lambda a: a["name"],
            PlacementProperties.VCPUS_AVAIL: lambda a: a["vcpu_avail"],
            PlacementProperties.MEMORY_MB_AVAIL: lambda a: a["memory_mb_avail"],
            PlacementProperties.DISK_GB_AVAIL: lambda a: a["disk_gb_avail"],
            PlacementProperties.VCPUS_USED: lambda a: a["vcpu_used"],
            PlacementProperties.MEMORY_MB_USED: lambda a: a["memory_mb_used"],
            PlacementProperties.DISK_GB_USED: lambda a: a["disk_gb_used"],
        }
        try:
            return mapping[prop]
        except KeyError as exp:
            raise QueryPropertyMappingError(
                f"Error: failed to get property mapping, property {prop.name} is not supported in PlacementProperties"
            ) from exp

    @staticmethod
    def get_marker_prop_func():
        """
        A getter method to return marker property function for pagination
        """
        return PlacementProperties.get_prop_mapping(
            PlacementProperties.RESOURCE_PROVIDER_ID
        )
