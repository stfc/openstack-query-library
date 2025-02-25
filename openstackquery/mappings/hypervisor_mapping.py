from typing import Type

from aliases import QueryChainMappings
from openstackquery.enums.props.hypervisor_properties import HypervisorProperties
from openstackquery.enums.props.server_properties import ServerProperties

from openstackquery.enums.query_presets import QueryPresets

from openstackquery.handlers.client_side_handler import ClientSideHandler
from openstackquery.handlers.server_side_handler import ServerSideHandler
from openstackquery.mappings.mapping_interface import MappingInterface

from openstackquery.runners.hypervisor_runner import HypervisorRunner
from openstackquery.runners.runner_wrapper import RunnerWrapper


class HypervisorMapping(MappingInterface):
    """
    Mapping class for querying Openstack Hypervisor objects
    Define property mappings, kwarg mappings and filter function mappings,
    and runner mapping related to hypervisors here
    """

    @staticmethod
    def get_chain_mappings() -> QueryChainMappings:
        """
        Should return a dictionary containing property pairs mapped to query mappings.
        This is used to define how to chain results from this query to other possible queries
        """
        return {
            HypervisorProperties.HYPERVISOR_NAME: [
                ServerProperties.HYPERVISOR_NAME,
            ]
        }

    @staticmethod
    def get_runner_mapping() -> Type[RunnerWrapper]:
        """
        Returns a mapping to associated Runner class for the Query (HypervisorRunner)
        """
        return HypervisorRunner

    @staticmethod
    def get_prop_mapping() -> Type[HypervisorProperties]:
        """
        Returns a mapping of valid presets for server side attributes (HypervisorProperties)
        """
        return HypervisorProperties

    @staticmethod
    def get_server_side_handler() -> ServerSideHandler:
        """
        method to configure a server handler which can be used to get 'filter' keyword arguments that
        can be passed to openstack function conn.compute.hypervisors() to filter results for a valid preset-property
        pair

        valid filters documented here:
            https://docs.openstack.org/openstacksdk/latest/user/proxies/compute.html
            https://docs.openstack.org/api-ref/compute/?expanded=list-hypervisors-detail
        """
        # No server-side filters for HypervisorQuery
        return ServerSideHandler({})

    @staticmethod
    def get_client_side_handler() -> ClientSideHandler:
        """
        This function returns a client-side handler object which can be used to handle filtering results locally.
        This function maps which properties are valid for each filter preset.
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
        return ClientSideHandler(
            {
                QueryPresets.EQUAL_TO: ["*"],
                QueryPresets.NOT_EQUAL_TO: ["*"],
                QueryPresets.ANY_IN: ["*"],
                QueryPresets.NOT_ANY_IN: ["*"],
                QueryPresets.MATCHES_REGEX: [
                    HypervisorProperties.HYPERVISOR_IP,
                    HypervisorProperties.HYPERVISOR_NAME,
                    HypervisorProperties.HYPERVISOR_DISABLED_REASON,
                ],
                QueryPresets.LESS_THAN: integer_prop_list,
                QueryPresets.GREATER_THAN: integer_prop_list,
                QueryPresets.LESS_THAN_OR_EQUAL_TO: integer_prop_list,
                QueryPresets.GREATER_THAN_OR_EQUAL_TO: integer_prop_list,
            }
        )
