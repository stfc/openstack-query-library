import logging
from typing import List, Optional, Tuple, Union

from openstackquery.aliases import (
    ClientSideFilterFunc,
    ClientSidePresetPropertyMappings,
    FilterFunc,
    FilterParams,
    OpenstackResourceObj,
    PropFunc,
)
from openstackquery.enums.props.prop_enum import PropEnum
from openstackquery.enums.query_presets import QueryPresets
from openstackquery.exceptions.parse_query_error import ParseQueryError
from openstackquery.exceptions.query_preset_mapping_error import QueryPresetMappingError
from openstackquery.handlers.client_side_filters import (
    prop_any_in,
    prop_equal_to,
    prop_greater_than,
    prop_greater_than_or_equal_to,
    prop_less_than,
    prop_less_than_or_equal_to,
    prop_matches_regex,
    prop_not_any_in,
    prop_not_equal_to,
    prop_not_matches_regex,
    prop_older_than,
    prop_older_than_or_equal_to,
    prop_younger_than,
    prop_younger_than_or_equal_to,
)
from openstackquery.handlers.handler_base import HandlerBase

logger = logging.getLogger(__name__)


class ClientSideHandler(HandlerBase):
    """
    Base class for subclasses that handle client-side filtering.
    This class stores a dictionary which maps preset/property pairs to a filter function that will be used after
    listing openstack resources
    """

    def __init__(
        self,
        preset_prop_mappings: ClientSidePresetPropertyMappings,
    ):
        self._filter_function_mappings = preset_prop_mappings
        self._filter_functions = {
            QueryPresets.OLDER_THAN: prop_older_than,
            QueryPresets.YOUNGER_THAN: prop_younger_than,
            QueryPresets.OLDER_THAN_OR_EQUAL_TO: prop_older_than_or_equal_to,
            QueryPresets.YOUNGER_THAN_OR_EQUAL_TO: prop_younger_than_or_equal_to,
            QueryPresets.ANY_IN: prop_any_in,
            QueryPresets.EQUAL_TO: prop_equal_to,
            QueryPresets.NOT_ANY_IN: prop_not_any_in,
            QueryPresets.NOT_EQUAL_TO: prop_not_equal_to,
            QueryPresets.GREATER_THAN: prop_greater_than,
            QueryPresets.LESS_THAN: prop_less_than,
            QueryPresets.GREATER_THAN_OR_EQUAL_TO: prop_greater_than_or_equal_to,
            QueryPresets.LESS_THAN_OR_EQUAL_TO: prop_less_than_or_equal_to,
            QueryPresets.MATCHES_REGEX: prop_matches_regex,
            QueryPresets.NOT_MATCHES_REGEX: prop_not_matches_regex,
        }

    def get_supported_props(self, preset: QueryPresets) -> Union[List, List[PropEnum]]:
        """
        Gets a list of all supported properties for a given preset
        """
        return list(self._filter_function_mappings[preset])

    def check_supported(self, preset: QueryPresets, prop: PropEnum) -> bool:
        """
        Method that returns True if filter function exists for a preset-property pair
        :param preset: A QueryPreset Enum for which a client-side filter function mapping may exist for
        :param prop: A property Enum for which a client-side filter function mapping may exist for
        """
        if not self.preset_known(preset):
            return False

        if prop in self._filter_function_mappings[preset]:
            return True

        # '*' represents that all props are valid for preset
        if ["*"] == self._filter_function_mappings[preset]:
            return True

        return False

    def preset_known(self, preset: QueryPresets) -> bool:
        """
        Method that returns True if a preset is known to the handler
        :param preset: A QueryPreset Enum which may have filter function mappings known to the handler
        """
        return preset in self._filter_function_mappings.keys()

    def get_filter_func(
        self,
        preset: QueryPresets,
        prop: PropEnum,
        prop_func: PropFunc,
        filter_func_kwargs: Optional[FilterParams] = None,
    ) -> Optional[ClientSideFilterFunc]:
        """
        Method that checks and returns a parsed filter function (if a mapping exists in this handler).
        the parsed filter function will take as input a single openstack resource and return
        True if resources passes check, False if not.

        :param preset: A QueryPreset Enum for which a filter function mapping may exist for
        :param prop: A property Enum for which a filter function mapping may exist for
        :param prop_func: A function to get a property of an openstack resource when given it as input
        :param filter_func_kwargs: A dictionary of keyword: argument pairs to pass into filter function
        """

        filter_func = None
        if self.check_supported(preset, prop):
            filter_func = self._filter_functions.get(preset, None)

        if not filter_func:
            logger.error(
                "Error: If you are here as a developer - "
                "you have likely not forgotten to add a mapping for the preset %s and property %s pair.\n"
                "\t- check the _get_client_side_handlers in <Resource>Query class",
                preset.name,
                prop.name,
            )

            logger.error(
                "Error: If you are here as a user - "
                "double check whether the preset %s is compatible with the property %s you're querying by.\n"
                "\t- i.e. using LESS_THAN on User property USER_NAME will not work since USER_NAME property "
                "is not an integer.\n"
                "\t- however, if you believe the preset should be compatible with the property please raise an "
                "issue with the repo maintainer",
                preset.name,
                prop.name,
            )

            raise QueryPresetMappingError(
                "Preset Not Found: failed to find filter_function mapping for preset "
                f"'{preset.name}' and property '{prop.name}'"
                "does the preset work with property specified?"
            )

        logger.debug(
            "found client-side filter function for preset %s: prop %s pair",
            preset.name,
            prop.name,
        )

        filter_func_valid, reason = self._check_filter_func(
            filter_func, filter_func_kwargs
        )
        if not filter_func_valid:
            raise QueryPresetMappingError(
                "Preset Argument Error: failed to build client-side filter function for preset:prop: "
                f"'{preset.name}':'{prop.name}' "
                f"reason: {reason}"
            )

        return lambda resource: self._filter_func_wrapper(
            resource, filter_func, prop_func, filter_func_kwargs
        )

    @staticmethod
    def _filter_func_wrapper(
        item: OpenstackResourceObj,
        selected_filter_func: FilterFunc,
        selected_prop_func: PropFunc,
        filter_func_kwargs: Optional[FilterParams] = None,
    ) -> bool:
        """
        Method that acts as a wrapper to a filter function, if the property cannot be found for the resource
        we return False before calling the filter function - since there's no property to compare.
        :param item: An openstack resource item
        :param selected_filter_func: The selected filter function to run if property given can be retrieved from
        given openstack resource
        :param selected_prop_func: The selected prop function to run to get property from given openstack resource
        :param **filter_func_kwargs: A dictionary of keyword args to configure selected filter function
        """
        try:
            item_prop = selected_prop_func(item)
        except (AttributeError, KeyError):
            return False
        if not filter_func_kwargs:
            filter_func_kwargs = {}
        return selected_filter_func(item_prop, **filter_func_kwargs)

    @staticmethod
    def _check_filter_func(
        func: FilterFunc, func_kwargs: Optional[FilterParams] = None
    ) -> Tuple[bool, str]:
        """
        Method checks a given function can accept a set of kwargs as arguments - using the EAFP principle.
        returns false and the error string if an error is raised - else true
        :param func: function to test
        :param func_kwargs: kwargs to test
        """

        # Try to run the filter function with "prop" = None.
        # The filter function should still work with prop as None
        if not func_kwargs:
            func_kwargs = {}
        try:
            func(None, **func_kwargs)
            return True, ""
        except (
            TypeError,
            NameError,
            ParseQueryError,
        ) as exp:
            return False, str(exp)
