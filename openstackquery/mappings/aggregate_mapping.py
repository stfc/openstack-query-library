from typing import Type

from openstackquery.aliases import QueryChainMappings
from openstackquery.enums.props.aggregate_properties import AggregateProperties
from openstackquery.enums.query_presets import QueryPresets
from openstackquery.handlers.client_side_handler import ClientSideHandler
from openstackquery.handlers.server_side_handler import ServerSideHandler
from openstackquery.mappings.mapping_interface import MappingInterface
from openstackquery.runners.aggregate_runner import AggregateRunner


class AggregateMapping(MappingInterface):
    """
    Mapping class for querying Openstack Aggregate objects
    Define property mappings, kwarg mappings and filter function mappings,
    and runner mapping related to aggregates here
    """

    @staticmethod
    def get_chain_mappings() -> QueryChainMappings:
        """
        Should return a dictionary containing property pairs mapped to query mappings.
        This is used to define how to chain results from this query to other possible queries
        """
        # TODO: find a way to map list of hostnames:
        #  AggregateProperties.HOST_IPS to HypervisorProperties.HYPERVISOR_NAME
        return None

    @staticmethod
    def get_runner_mapping() -> Type[AggregateRunner]:
        """
        Returns a mapping to associated Runner class for the Query (AggregateRunner)
        """
        return AggregateRunner

    @staticmethod
    def get_prop_mapping() -> Type[AggregateProperties]:
        """
        Returns a mapping of valid presets for server side attributes (HypervisorProperties)
        """
        return AggregateProperties

    @staticmethod
    def get_server_side_handler() -> ServerSideHandler:
        """
        method to configure a server handler which can be used to get 'filter' keyword arguments that
        can be passed to openstack function conn.compute.aggregates() to filter results for a valid preset-property
        pair

        valid filters documented here:
            https://docs.openstack.org/openstacksdk/latest/user/proxies/compute.html
            https://docs.openstack.org/api-ref/compute/?expanded=list-hypervisors-detail#list-aggregates
        """
        # No server-side filters for AggregateQuery
        return ServerSideHandler({})

    @staticmethod
    def get_client_side_handlers() -> ClientSideHandler:
        """
        method to configure a set of client-side handlers which can be used to get local filter functions
        corresponding to valid preset-property pairs. These filter functions can be used to filter results after
        listing all aggregates.
        """
        date_prop_list = [
            AggregateProperties.AGGREGATE_DELETED_AT,
            AggregateProperties.AGGREGATE_UPDATED_AT,
            AggregateProperties.AGGREGATE_CREATED_AT,
        ]

        string_prop_list = [
            AggregateProperties.AGGREGATE_HOSTTYPE,
            AggregateProperties.AGGREGATE_HOST_IPS,
            AggregateProperties.AGGREGATE_METADATA,
            AggregateProperties.AGGREGATE_LOCAL_STORAGE_TYPE,
        ]

        return ClientSideHandler(
            {
                QueryPresets.EQUAL_TO: ["*"],
                QueryPresets.NOT_EQUAL_TO: ["*"],
                QueryPresets.ANY_IN: ["*"],
                QueryPresets.NOT_ANY_IN: ["*"],
                QueryPresets.MATCHES_REGEX: string_prop_list,
                QueryPresets.NOT_MATCHES_REGEX: string_prop_list,
                QueryPresets.YOUNGER_THAN: date_prop_list,
                QueryPresets.YOUNGER_THAN_OR_EQUAL_TO: date_prop_list,
                QueryPresets.OLDER_THAN: date_prop_list,
                QueryPresets.OLDER_THAN_OR_EQUAL_TO: date_prop_list,
                QueryPresets.LESS_THAN: [AggregateProperties.AGGREGATE_GPUNUM],
                QueryPresets.LESS_THAN_OR_EQUAL_TO: [
                    AggregateProperties.AGGREGATE_GPUNUM
                ],
                QueryPresets.GREATER_THAN: [AggregateProperties.AGGREGATE_GPUNUM],
                QueryPresets.GREATER_THAN_OR_EQUAL_TO: [
                    AggregateProperties.AGGREGATE_GPUNUM
                ],
            }
        )
