from typing import Type

from openstackquery.aliases import QueryChainMappings
from openstackquery.enums.props.flavor_properties import FlavorProperties
from openstackquery.enums.props.server_properties import ServerProperties
from openstackquery.enums.query_presets import QueryPresets
from openstackquery.handlers.client_side_handler import ClientSideHandler
from openstackquery.handlers.server_side_handler import ServerSideHandler
from openstackquery.mappings.mapping_interface import MappingInterface
from openstackquery.runners.flavor_runner import FlavorRunner


class FlavorMapping(MappingInterface):
    """
    Mapping class for querying Openstack Flavor objects
    Define property mappings, kwarg mappings and filter function mappings, and runner mapping related to flavors here
    """

    @staticmethod
    def get_chain_mappings() -> QueryChainMappings:
        """
        Should return a dictionary containing property pairs mapped to query mappings.
        This is used to define how to chain results from this query to other possible queries
        """
        return {
            FlavorProperties.FLAVOR_ID: [ServerProperties.FLAVOR_ID],
        }

    @staticmethod
    def get_runner_mapping() -> Type[FlavorRunner]:
        """
        Returns a mapping to associated Runner class for the Query (FlavorRunner)
        """
        return FlavorRunner

    @staticmethod
    def get_prop_mapping() -> Type[FlavorProperties]:
        """
        Returns a mapping of valid presets for server side attributes (FlavorProperties)
        """
        return FlavorProperties

    @staticmethod
    def get_server_side_handler() -> ServerSideHandler:
        """
        method to configure a server handler which can be used to get 'filter' keyword arguments that
        can be passed to openstack function conn.compute.flavors() to filter results for a valid preset-property pair

        valid filters documented here:
            https://docs.openstack.org/openstacksdk/latest/user/proxies/compute.html
            https://docs.openstack.org/api-ref/compute/?expanded=list-servers-detail#show-flavor-details
        """
        return ServerSideHandler(
            {
                QueryPresets.EQUAL_TO: {
                    FlavorProperties.FLAVOR_IS_PUBLIC: lambda value: {
                        "is_public": value
                    }
                },
                QueryPresets.NOT_EQUAL_TO: {
                    FlavorProperties.FLAVOR_IS_PUBLIC: lambda value: {
                        "is_public": not value
                    }
                },
                QueryPresets.LESS_THAN_OR_EQUAL_TO: {
                    FlavorProperties.FLAVOR_DISK: lambda value: {"minDisk": int(value)},
                    FlavorProperties.FLAVOR_RAM: lambda value: {"minRam": int(value)},
                },
            }
        )

    @staticmethod
    def get_client_side_handler() -> ClientSideHandler:
        """
        This function returns a client-side handler object which can be used to handle filtering results locally.
        This function maps which properties are valid for each filter preset.
        """
        integer_prop_list = [
            FlavorProperties.FLAVOR_RAM,
            FlavorProperties.FLAVOR_DISK,
            FlavorProperties.FLAVOR_EPHEMERAL,
            FlavorProperties.FLAVOR_SWAP,
            FlavorProperties.FLAVOR_VCPU,
        ]
        return ClientSideHandler(
            # set generic query preset mappings
            {
                QueryPresets.EQUAL_TO: ["*"],
                QueryPresets.NOT_EQUAL_TO: ["*"],
                QueryPresets.ANY_IN: ["*"],
                QueryPresets.NOT_ANY_IN: ["*"],
                QueryPresets.MATCHES_REGEX: [FlavorProperties.FLAVOR_NAME],
                QueryPresets.NOT_MATCHES_REGEX: [FlavorProperties.FLAVOR_NAME],
                QueryPresets.LESS_THAN: integer_prop_list,
                QueryPresets.LESS_THAN_OR_EQUAL_TO: integer_prop_list,
                QueryPresets.GREATER_THAN: integer_prop_list,
                QueryPresets.GREATER_THAN_OR_EQUAL_TO: integer_prop_list,
            }
        )
