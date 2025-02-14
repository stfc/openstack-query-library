from typing import Type

from aliases import QueryChainMappings
from enums.props.server_properties import ServerProperties
from openstackquery.enums.props.hypervisor_properties import HypervisorProperties
from openstackquery.enums.props.placement_properties import PlacementProperties
from openstackquery.enums.props.prop_enum import PropEnum
from openstackquery.enums.query_presets import (
    QueryPresetsGeneric,
    QueryPresetsString,
    QueryPresetsInteger,
)
from openstackquery.handlers.client_side_handler_generic import (
    ClientSideHandlerGeneric,
)
from openstackquery.handlers.client_side_handler_integer import (
    ClientSideHandlerInteger,
)
from openstackquery.handlers.client_side_handler_string import ClientSideHandlerString
from openstackquery.handlers.server_side_handler import ServerSideHandler
from openstackquery.mappings.mapping_interface import MappingInterface
from openstackquery.runners.placement_runner import PlacementRunner

from openstackquery.runners.runner_wrapper import RunnerWrapper
from openstackquery.structs.query_client_side_handlers import QueryClientSideHandlers


class PlacementMapping(MappingInterface):
    """
    Mapping class for querying Openstack placement and resource objects
    Define property mappings, kwarg mappings and filter function mappings,
    and runner mapping related to placement and resources here
    """

    @staticmethod
    def get_chain_mappings() -> QueryChainMappings:
        """
        Should return a dictionary containing property pairs mapped to query mappings.
        This is used to define how to chain results from this query to other possible queries
        """
        return {
            PlacementProperties.RESOURCE_PROVIDER_NAME: [
                HypervisorProperties.HYPERVISOR_NAME,
                ServerProperties.HYPERVISOR_NAME,
            ]
        }

    @staticmethod
    def get_runner_mapping() -> Type[RunnerWrapper]:
        """
        Returns a mapping to associated Runner class for the Query (placement and resourceRunner)
        """
        return PlacementRunner

    @staticmethod
    def get_prop_mapping() -> Type[PropEnum]:
        """
        Returns a mapping of valid presets for server side attributes (placement and resourceProperties)
        """
        return PlacementProperties

    @staticmethod
    def get_server_side_handler() -> ServerSideHandler:
        """
        method to configure a server handler which can be used to get 'filter' keyword arguments that
        can be passed to openstack function conn.placement.resource_providers() to filter results
        Valid filters documented here:
            https://docs.openstack.org/openstacksdk/latest/user/proxies/placement.html
        """
        return ServerSideHandler(
            {
                QueryPresetsGeneric.EQUAL_TO: {
                    PlacementProperties.RESOURCE_PROVIDER_ID: lambda value: {
                        "id": value
                    },
                    PlacementProperties.RESOURCE_PROVIDER_NAME: lambda value: {
                        "name": value
                    },
                }
            }
        )

    @staticmethod
    def get_client_side_handlers() -> QueryClientSideHandlers:
        """
        method to configure a set of client-side handlers which can be used to get local filter functions
        corresponding to valid preset-property pairs. These filter functions can be used to filter results after
        listing all placement and resources.
        """
        integer_prop_list = [
            PlacementProperties.VCPUS_AVAIL,
            PlacementProperties.MEMORY_MB_AVAIL,
            PlacementProperties.DISK_GB_AVAIL,
            PlacementProperties.VCPUS_USED,
            PlacementProperties.MEMORY_MB_USED,
            PlacementProperties.DISK_GB_USED,
        ]

        return QueryClientSideHandlers(
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
                        PlacementProperties.RESOURCE_PROVIDER_ID,
                        PlacementProperties.RESOURCE_PROVIDER_NAME,
                    ]
                }
            ),
            datetime_handler=None,
            integer_handler=ClientSideHandlerInteger(
                {
                    QueryPresetsInteger.LESS_THAN: integer_prop_list,
                    QueryPresetsInteger.LESS_THAN_OR_EQUAL_TO: integer_prop_list,
                    QueryPresetsInteger.GREATER_THAN: integer_prop_list,
                    QueryPresetsInteger.GREATER_THAN_OR_EQUAL_TO: integer_prop_list,
                }
            ),
        )
