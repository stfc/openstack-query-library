from typing import Optional, Dict, Any, Type, Union
import logging

from openstackquery.handlers.client_side_handler import ClientSideHandler
from openstackquery.handlers.server_side_handler import ServerSideHandler

from openstackquery.enums.query_presets import QueryPresets
from openstackquery.enums.props.prop_enum import PropEnum

from openstackquery.exceptions.query_preset_mapping_error import QueryPresetMappingError
from openstackquery.exceptions.query_property_mapping_error import (
    QueryPropertyMappingError,
)

from openstackquery.aliases import (
    ClientSideFilterFunc,
    ClientSideFilters,
    ServerSideFilters,
)


logger = logging.getLogger(__name__)


class QueryBuilder:
    """
    Helper class to handle setting and validating query parameters - primarily parsing 'where()' arguments to get
    filter function or kwarg params to use when running query
    """

    def __init__(
        self,
        prop_enum_cls: Type[PropEnum],
        client_side_handler: ClientSideHandler,
        server_side_handler: Optional[ServerSideHandler],
    ):
        self._client_side_handler = client_side_handler
        self._prop_enum_cls = prop_enum_cls
        self._server_side_handler = server_side_handler

        self._client_side_filters = []
        self._server_side_filters = []
        self._server_filter_fallback = []

    @property
    def client_side_filters(self) -> Optional[ClientSideFilters]:
        """
        a getter method to return the client-side filter function
        """
        return self._client_side_filters

    @client_side_filters.setter
    def client_side_filters(self, client_filters: ClientSideFilters):
        """
        a setter method to set client side filter function
        :param client_filters: a list of filter functions that each take an openstack resource object and return
        True if it matches filter, False if not
        """
        self._client_side_filters = client_filters

    @property
    def server_side_filters(self) -> Optional[ServerSideFilters]:
        """
        a getter method to return server-side filters to pass to openstacksdk
        """
        return self._server_side_filters

    @server_side_filters.setter
    def server_side_filters(self, server_filters: ServerSideFilters):
        """
        a setter method to set server side filters
        :param server_filters: a list of server-side-filters that holds filter options to pass to openstacksdk
        """
        self._server_side_filters = server_filters

    @property
    def server_filter_fallback(self):
        """
        a getter method to return equivalent client-side filters for each server-side filter if
        server-side filters are not to be used
        """
        return self._server_filter_fallback

    @server_filter_fallback.setter
    def server_filter_fallback(self, fallback_filters: ClientSideFilters):
        """
        a setter method to set client-side filters to fallback on for each server-side filter if
        server-side filters are not to be used
        :param fallback_filters: a set of client-side filters
        """
        self._server_filter_fallback = fallback_filters

    def _parse_where_inputs(self, preset, prop):
        """
        method converts where() 'preset' and 'prop' user inputs into Enums, any string aliases will
        be converted into Enums
        :param preset: Name of query preset to use
        :param prop: Name of property that the query preset will act on
        """
        if isinstance(preset, str):
            preset = QueryPresets.from_string(preset)
        if isinstance(prop, str):
            prop = self._prop_enum_cls.from_string(prop)
        return preset, prop

    def parse_where(
        self,
        preset: Union[str, QueryPresets],
        prop: Union[str, PropEnum],
        preset_kwargs: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        method which parses and builds a filter function and (if possible) a set of openstack filter kwargs that
        corresponds to a given preset, property and set of preset arguments
        :param preset: Name of query preset to use
        :param prop: Name of property that the query preset will act on
        :param preset_kwargs: A set of arguments to pass to configure filter function and filter kwargs
        """
        preset, prop = self._parse_where_inputs(preset, prop)
        self._validate_where(preset, prop)

        prop_func = self._prop_enum_cls.get_prop_mapping(prop)

        if not prop_func:
            logging.error(
                "Error: If you are here as a developer"
                "you have likely forgotten to add a prop mapping for the property '%s'"
                "under queries/<resource>_query",
                prop.name,
            )

            raise QueryPropertyMappingError(
                f"""
                Error: failed to get property mapping, given property
                {prop.name} is not supported in prop_handler
                """
            )

        client_side_filter = self._client_side_handler.get_filter_func(
            preset=preset,
            prop=prop,
            prop_func=prop_func,
            filter_func_kwargs=preset_kwargs,
        )

        server_side_filters = self._server_side_handler.get_filters(
            preset=preset, prop=prop, params=preset_kwargs
        )

        if not server_side_filters:
            logger.info(
                "No server-side filters for preset '%s': prop '%s' pair "
                "- using client-side filter - this may take longer",
                preset.name,
                prop.name,
            )
        else:
            logger.info(
                "Found %s set of server-side filters for preset '%s': prop '%s' pair",
                len(server_side_filters),
                preset.name,
                prop.name,
            )

        logger.debug(
            "server-side-filters found: %s",
            {f"{server_side_filters}" if server_side_filters else "None"},
        )
        logger.debug(
            "client-side-filter found: %s",
            {client_side_filter if client_side_filter else "None"},
        )

        self._add_filter(
            client_side_filter=client_side_filter,
            server_side_filters=server_side_filters,
        )

    def _validate_where(self, preset: QueryPresets, prop: PropEnum) -> None:
        """
        helper function for parse_where
        validates that the given property can be used with given preset, raises errors if not
        :param preset: A given preset that describes the query type
        :param prop: A prop which the preset will act on
        """

        # Most likely we have forgotten to add a mapping for a preset at the client-side
        # All presets should have a client-side handler associated to it
        if not self._client_side_handler.preset_known(preset):
            logger.error(
                "Error: If you are here as a developer "
                "you have likely not forgotten to instantiate a client-side handler for the "
                "preset '%s'",
                preset.name,
            )

            logger.error(
                "Error: If you are here as a user - double check whether the preset '%s' is compatible"
                "with the resource you're querying.\n "
                "i.e. using LESS_THAN for querying Users "
                "(as users holds no query-able properties which are of an integer type).\n "
                "However, if you believe it should, please raise an issue with the repo maintainer.",
                preset.name,
            )

            raise QueryPresetMappingError(
                f"No client-side handler found for preset '{preset.name}' - property '{prop.name}' pair "
                f"- resource likely does not support querying using this preset"
            )

        if not self._client_side_handler.check_supported(preset, prop):
            logger.error(
                "Error: if you are here as a developer "
                "you have likely forgotten to add client-side mappings for the preset '%s' and property '%s' "
                "under mappings/<resource>_mapping",
                preset.name,
                prop.name,
            )

            logger.error(
                "Error: If you are here as a user - double check whether the property '%s' can be used "
                "with the preset '%s' \n"
                "i.e. using LESS_THAN with a string property like SERVER_NAME won't work "
                "(server_name holds strings, and preset LESS_THAN only works on integers.)\n "
                "However, if you believe the preset and property should be used together please raise an "
                "issue with the repo maintainer",
                prop.name,
                preset.name,
            )

            raise QueryPresetMappingError(
                f"No client-side handler found which supports preset '{preset.name}' and property '{prop.name}"
            )

    def _add_filter(
        self,
        client_side_filter: ClientSideFilterFunc,
        server_side_filters: Optional[ServerSideFilters] = None,
    ) -> None:
        """
        method which parses client-side and server-side filters for a given preset and adds it to the
        list of query operations to perform
        :param client_side_filter: A client side filter function for the query preset
        :param server_side_filters: An optional set of server side filters for the query preset
        """

        # add as client_side_filter if no server_side_filter
        if not server_side_filters:
            self.client_side_filters.append(client_side_filter)
            return

        # If the keys of the new filter and current filter match but the values are different - then the filter
        # will likely return nothing - this is not for us to enforce - hence add it as a client-side-filter
        # if the values also match - just ignore it as a duplicate
        for current_server_filter in self.server_side_filters:
            for new_server_filter in server_side_filters:
                if set(new_server_filter.keys()).intersection(
                    set(current_server_filter.keys())
                ):
                    self.client_side_filters.append(client_side_filter)
                    return

        # before adding server-side filter - set fallback
        self.server_filter_fallback.append(client_side_filter)

        # if there are no server-side filters - we don't need to aggregate with existing ones - we can just set it
        if not self.server_side_filters:
            self.server_side_filters = server_side_filters
            return

        # we aggregate the new filter with other server filters already set into
        self.server_side_filters = [
            {**new_server_filter, **current_server_filter}
            for current_server_filter in self.server_side_filters
            for new_server_filter in server_side_filters
        ]
