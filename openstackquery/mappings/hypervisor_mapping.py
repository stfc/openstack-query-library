from typing import Type

from aliases import QueryChainMappings
from openstackquery.enums.props.hypervisor_properties import HypervisorProperties
from openstackquery.enums.props.server_properties import ServerProperties
from openstackquery.enums.query_presets import (
    QueryPresetsGeneric,
    QueryPresetsString,
    QueryPresetsInteger,
)
from openstackquery.handlers.client_side_handler_generic import (
    ClientSideHandlerGeneric,
)
from openstackquery.handlers.client_side_handler_string import ClientSideHandlerString
from openstackquery.handlers.client_side_handler_integer import ClientSideHandlerInteger

from openstackquery.handlers.server_side_handler import ServerSideHandler
from openstackquery.mappings.mapping_interface import MappingInterface

from openstackquery.runners.hypervisor_runner import HypervisorRunner
from openstackquery.runners.runner_wrapper import RunnerWrapper
from openstackquery.structs.query_client_side_handlers import QueryClientSideHandlers


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
    def get_client_side_handlers() -> QueryClientSideHandlers:
        """
        method to configure a set of client-side handlers which can be used to get local filter functions
        corresponding to valid preset-property pairs. These filter functions can be used to filter results after
        listing all hypervisors.
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

        return QueryClientSideHandlers(
            # set generic query preset mappings
            generic_handler=ClientSideHandlerGeneric(
                {
                    QueryPresetsGeneric.EQUAL_TO: ["*"],
                    QueryPresetsGeneric.NOT_EQUAL_TO: ["*"],
                    QueryPresetsGeneric.ANY_IN: ["*"],
                    QueryPresetsGeneric.NOT_ANY_IN: ["*"],
                }
            ),
            # set string query preset mappings
            string_handler=ClientSideHandlerString(
                {
                    QueryPresetsString.MATCHES_REGEX: [
                        HypervisorProperties.HYPERVISOR_IP,
                        HypervisorProperties.HYPERVISOR_NAME,
                        HypervisorProperties.HYPERVISOR_DISABLED_REASON,
                    ]
                }
            ),
            # set datetime query preset mappings
            datetime_handler=None,
            # set integer query preset mappings
            integer_handler=ClientSideHandlerInteger(
                {
                    QueryPresetsInteger.LESS_THAN: integer_prop_list,
                    QueryPresetsInteger.LESS_THAN_OR_EQUAL_TO: integer_prop_list,
                    QueryPresetsInteger.GREATER_THAN: integer_prop_list,
                    QueryPresetsInteger.GREATER_THAN_OR_EQUAL_TO: integer_prop_list,
                }
            ),
        )
