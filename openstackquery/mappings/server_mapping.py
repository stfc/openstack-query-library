from typing import Type
from openstackquery.aliases import QueryChainMappings

from openstackquery.enums.props.server_properties import ServerProperties
from openstackquery.enums.query_presets import QueryPresets

from openstackquery.enums.props.user_properties import UserProperties
from openstackquery.enums.props.project_properties import ProjectProperties
from openstackquery.enums.props.flavor_properties import FlavorProperties
from openstackquery.enums.props.image_properties import ImageProperties
from openstackquery.enums.props.hypervisor_properties import HypervisorProperties

from openstackquery.handlers.client_side_handler import ClientSideHandler
from openstackquery.handlers.server_side_handler import ServerSideHandler

from openstackquery.mappings.mapping_interface import MappingInterface
from openstackquery.runners.server_runner import ServerRunner

from openstackquery.time_utils import TimeUtils


class ServerMapping(MappingInterface):
    """
    Mapping class for querying Openstack Server objects.
    Define property mappings, kwarg mappings and filter function mappings, and runner mapping related to servers here
    """

    @staticmethod
    def get_chain_mappings() -> QueryChainMappings:
        """
        Should return a dictionary containing property pairs mapped to query mappings.
        This is used to define how to chain results from this query to other possible queries
        """
        return {
            ServerProperties.USER_ID: [UserProperties.USER_ID],
            ServerProperties.PROJECT_ID: [ProjectProperties.PROJECT_ID],
            ServerProperties.FLAVOR_ID: [FlavorProperties.FLAVOR_ID],
            ServerProperties.IMAGE_ID: [ImageProperties.IMAGE_ID],
            ServerProperties.HYPERVISOR_NAME: [
                HypervisorProperties.HYPERVISOR_NAME,
            ],
        }

    @staticmethod
    def get_runner_mapping() -> Type[ServerRunner]:
        """
        Returns a mapping to associated Runner class for the Query (ServerRunner)
        """
        return ServerRunner

    @staticmethod
    def get_prop_mapping() -> Type[ServerProperties]:
        """
        Returns a mapping of valid presets for server side attributes (ServerProperties)
        """
        return ServerProperties

    @staticmethod
    def get_server_side_handler() -> ServerSideHandler:
        """
        method to configure a server handler which can be used to get 'filter' keyword arguments that
        can be passed to openstack function conn.compute.servers() to filter results for a valid preset-property pair

        valid filters documented here:
            https://docs.openstack.org/openstacksdk/latest/user/proxies/compute.html
            https://docs.openstack.org/api-ref/compute/?expanded=list-servers-detail#list-server-request
        """
        return ServerSideHandler(
            {
                QueryPresets.EQUAL_TO: {
                    ServerProperties.USER_ID: lambda value: {"user_id": value},
                    ServerProperties.SERVER_ID: lambda value: {"uuid": value},
                    ServerProperties.SERVER_NAME: lambda value: {"hostname": value},
                    ServerProperties.SERVER_DESCRIPTION: lambda value: {
                        "description": value
                    },
                    ServerProperties.SERVER_STATUS: lambda value: {"status": value},
                    ServerProperties.SERVER_CREATION_DATE: lambda value: {
                        "created_at": value
                    },
                    ServerProperties.FLAVOR_ID: lambda value: {"flavor": value},
                    ServerProperties.IMAGE_ID: lambda value: {"image": value},
                    ServerProperties.PROJECT_ID: lambda value: {"project_id": value},
                },
                QueryPresets.ANY_IN: {
                    ServerProperties.USER_ID: lambda values: [
                        {"user_id": value} for value in values
                    ],
                    ServerProperties.SERVER_ID: lambda values: [
                        {"uuid": value} for value in values
                    ],
                    ServerProperties.SERVER_NAME: lambda values: [
                        {"hostname": value} for value in values
                    ],
                    ServerProperties.SERVER_DESCRIPTION: lambda values: [
                        {"description": value} for value in values
                    ],
                    ServerProperties.SERVER_STATUS: lambda values: [
                        {"status": value} for value in values
                    ],
                    ServerProperties.SERVER_CREATION_DATE: lambda values: [
                        {"created_at": value} for value in values
                    ],
                    ServerProperties.FLAVOR_ID: lambda values: [
                        {"flavor": value} for value in values
                    ],
                    ServerProperties.IMAGE_ID: lambda values: [
                        {"image": value} for value in values
                    ],
                    ServerProperties.PROJECT_ID: lambda values: [
                        {"project_id": value} for value in values
                    ],
                },
                QueryPresets.OLDER_THAN_OR_EQUAL_TO: {
                    ServerProperties.SERVER_LAST_UPDATED_DATE: lambda func=TimeUtils.convert_to_timestamp, **kwargs: {
                        "changes-before": func(**kwargs)
                    }
                },
                QueryPresets.YOUNGER_THAN_OR_EQUAL_TO: {
                    ServerProperties.SERVER_LAST_UPDATED_DATE: lambda func=TimeUtils.convert_to_timestamp, **kwargs: {
                        "changes-since": func(**kwargs)
                    }
                },
            }
        )

    @staticmethod
    def get_client_side_handler() -> ClientSideHandler:
        """
        This function returns a client-side handler object which can be used to handle filtering results locally.
        This function maps which properties are valid for each filter preset.
        """
        return ClientSideHandler(
            {
                QueryPresets.EQUAL_TO: ["*"],
                QueryPresets.NOT_EQUAL_TO: ["*"],
                QueryPresets.ANY_IN: ["*"],
                QueryPresets.NOT_ANY_IN: ["*"],
                QueryPresets.MATCHES_REGEX: [
                    ServerProperties.SERVER_NAME,
                    ServerProperties.ADDRESSES,
                ],
                QueryPresets.OLDER_THAN: [
                    ServerProperties.SERVER_CREATION_DATE,
                    ServerProperties.SERVER_LAST_UPDATED_DATE,
                ],
                QueryPresets.YOUNGER_THAN: [
                    ServerProperties.SERVER_CREATION_DATE,
                    ServerProperties.SERVER_LAST_UPDATED_DATE,
                ],
                QueryPresets.YOUNGER_THAN_OR_EQUAL_TO: [
                    ServerProperties.SERVER_CREATION_DATE,
                    ServerProperties.SERVER_LAST_UPDATED_DATE,
                ],
                QueryPresets.OLDER_THAN_OR_EQUAL_TO: [
                    ServerProperties.SERVER_CREATION_DATE,
                    ServerProperties.SERVER_LAST_UPDATED_DATE,
                ],
            }
        )
