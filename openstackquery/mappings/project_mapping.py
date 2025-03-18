from typing import Type
from openstackquery.aliases import QueryChainMappings
from openstackquery.enums.query_presets import QueryPresets

from openstackquery.enums.props.project_properties import ProjectProperties
from openstackquery.enums.props.server_properties import ServerProperties

from openstackquery.handlers.server_side_handler import ServerSideHandler
from openstackquery.handlers.client_side_handler import ClientSideHandler

from openstackquery.mappings.mapping_interface import MappingInterface
from openstackquery.runners.project_runner import ProjectRunner


class ProjectMapping(MappingInterface):
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
        return {ProjectProperties.PROJECT_ID: [ServerProperties.PROJECT_ID]}

    @staticmethod
    def get_runner_mapping() -> Type[ProjectRunner]:
        """
        Returns a mapping to associated Runner class for the Query (ProjectRunner)
        """
        return ProjectRunner

    @staticmethod
    def get_prop_mapping() -> Type[ProjectProperties]:
        """
        Returns a mapping of valid presets for server side attributes (ProjectProperties)
        """
        return ProjectProperties

    @staticmethod
    def get_server_side_handler() -> ServerSideHandler:
        """
        method to configure a server handler which can be used to get 'filter' keyword arguments that
        can be passed to openstack function conn.compute.flavors() to filter results for a valid preset-property pair

        valid filters documented here:
            https://docs.openstack.org/openstacksdk/latest/user/proxies/identity_v3.html
            https://docs.openstack.org/api-ref/identity/v3/index.html#list-projects
        """
        return ServerSideHandler(
            {
                QueryPresets.EQUAL_TO: {
                    ProjectProperties.PROJECT_ID: lambda value: {"id": value},
                    ProjectProperties.PROJECT_DOMAIN_ID: lambda value: {
                        "domain_id": value
                    },
                    ProjectProperties.PROJECT_IS_ENABLED: lambda value: {
                        "is_enabled": value
                    },
                    ProjectProperties.PROJECT_IS_DOMAIN: lambda value: {
                        "is_domain": value
                    },
                    ProjectProperties.PROJECT_NAME: lambda value: {"name": value},
                    ProjectProperties.PROJECT_PARENT_ID: lambda value: {
                        "parent_id": value
                    },
                },
                QueryPresets.NOT_EQUAL_TO: {
                    ProjectProperties.PROJECT_IS_ENABLED: lambda value: {
                        "is_enabled": not value
                    },
                    ProjectProperties.PROJECT_IS_DOMAIN: lambda value: {
                        "is_domain": not value
                    },
                },
                QueryPresets.ANY_IN: {
                    ProjectProperties.PROJECT_ID: lambda values: [
                        {"id": value} for value in values
                    ],
                    ProjectProperties.PROJECT_DOMAIN_ID: lambda values: [
                        {"domain_id": value} for value in values
                    ],
                    ProjectProperties.PROJECT_NAME: lambda values: [
                        {"name": value} for value in values
                    ],
                    ProjectProperties.PROJECT_PARENT_ID: lambda values: [
                        {"parent_id": value} for value in values
                    ],
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
                    ProjectProperties.PROJECT_NAME,
                    ProjectProperties.PROJECT_DESCRIPTION,
                ],
            }
        )
