from typing import Type

from aliases import QueryChainMappings
from openstackquery.structs.query_client_side_handlers import QueryClientSideHandlers

from openstackquery.enums.props.user_properties import UserProperties
from openstackquery.enums.query_presets import (
    QueryPresetsGeneric,
    QueryPresetsString,
)
from openstackquery.enums.props.server_properties import ServerProperties

from openstackquery.handlers.server_side_handler import ServerSideHandler


from openstackquery.handlers.client_side_handler_generic import (
    ClientSideHandlerGeneric,
)
from openstackquery.handlers.client_side_handler_string import ClientSideHandlerString

from openstackquery.mappings.mapping_interface import MappingInterface
from openstackquery.runners.user_runner import UserRunner


class UserMapping(MappingInterface):
    """
    Mapping class for querying Openstack User objects.
    Define property mappings, kwarg mappings, filter function mappings, and runner mappings related to users here
    """

    @staticmethod
    def get_chain_mappings() -> QueryChainMappings:
        """
        Should return a dictionary containing property pairs mapped to query mappings.
        This is used to define how to chain results from this query to other possible queries
        """
        return {UserProperties.USER_ID: [ServerProperties.USER_ID]}

    @staticmethod
    def get_runner_mapping() -> Type[UserRunner]:
        """
        Returns a mapping to associated Runner class for the Query (UserRunner)
        """
        return UserRunner

    @staticmethod
    def get_prop_mapping() -> Type[UserProperties]:
        """
        Returns a mapping of valid presets for server side attributes (UserProperties)
        """
        return UserProperties

    @staticmethod
    def get_server_side_handler() -> ServerSideHandler:
        """
        method to configure a server-side handler which can be used to get 'filter' keyword arguments that
        can be passed to an openstack function to filter results for a valid preset-property
        on the control plane, rather than locally.

        valid filters documented here:
            https://docs.openstack.org/openstacksdk/latest/user/proxies/identity_v3.html
            https://docs.openstack.org/api-ref/identity/v3/#list-users
        """
        return ServerSideHandler(
            {
                QueryPresetsGeneric.EQUAL_TO: {
                    UserProperties.USER_DOMAIN_ID: lambda value: {"domain_id": value},
                    UserProperties.USER_NAME: lambda value: {"name": value},
                    UserProperties.USER_ID: lambda value: {"id": value},
                },
                QueryPresetsGeneric.ANY_IN: {
                    UserProperties.USER_DOMAIN_ID: lambda values: [
                        {"domain_id": value} for value in values
                    ],
                    UserProperties.USER_NAME: lambda values: [
                        {"name": value} for value in values
                    ],
                    UserProperties.USER_ID: lambda values: [
                        {"id": value} for value in values
                    ],
                },
            }
        )

    @staticmethod
    def get_client_side_handlers() -> QueryClientSideHandlers:
        """
        method to configure a set of client-side handlers which can be used to get local filter functions
        corresponding to valid preset-property pairs. These filter functions can be used to filter results after
        listing all users.
        """
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
                        UserProperties.USER_EMAIL,
                        UserProperties.USER_NAME,
                    ]
                }
            ),
            # set datetime query preset mappings
            datetime_handler=None,
            # set integer query preset mappings
            integer_handler=None,
        )
