import logging
from copy import deepcopy
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Union

from openstackquery.aliases import OpenstackResourceObj, PropValue
from openstackquery.enums.props.prop_enum import PropEnum
from openstackquery.enums.query_presets import QueryPresets
from openstackquery.enums.sort_order import SortOrder
from openstackquery.exceptions.parse_query_error import ParseQueryError

if TYPE_CHECKING:
    from openstackquery.structs.query_components import QueryComponents

logger = logging.getLogger(__name__)


class QueryAPI:
    """
    Interface for Query Classes. This class exposes all public methods for query api.
    """

    def __init__(self, query_components: "QueryComponents"):
        self.builder = query_components.builder
        self.executor = query_components.executor
        self.parser = query_components.parser
        self.output = query_components.output
        self.chainer = query_components.chainer
        self.results_container = None

    def select(self, *props: Union[str, PropEnum]):
        """
        Public method used to 'select' properties that the query will return the value of.
        Mutually exclusive to returning objects using select_all()
        :param props: one or more properties to collect described as enum or a string that can convert to enum
        """

        # is an idempotent function
        # can be called multiple times with should aggregate properties to select
        if not props:
            raise ParseQueryError("provide at least one property to select")

        self.output.parse_select(*props, select_all=False)
        logger.debug(
            "selected props are now: %s",
            [prop.name for prop in self.output.selected_props],
        )
        return self

    def select_all(self):
        """
        Public method used to 'select' all properties that are available to be returned
        Mutually exclusive to returning objects using select_all()

        Overrides all currently selected properties
        returns list of properties currently selected
        """
        self.output.parse_select(select_all=True)
        logger.debug(
            "selected props are now: %s",
            [prop.name for prop in self.output.selected_props],
        )
        return self

    def where(
        self, preset: Union[str, QueryPresets], prop: Union[str, PropEnum], **kwargs
    ):
        """
        Public method used to set the conditions for the query.
        :param preset: QueryPreset Enum or string alias to use
        :param prop: Property Enum or string alias that the query preset will be used on
        :param kwargs: a set of optional arguments to pass along with the preset - property pair
            - these kwargs are dependent on the preset given
        """
        self.builder.parse_where(preset, prop, kwargs)
        return self

    def sort_by(self, *sort_by: Tuple[Union[PropEnum, str], Union[SortOrder, str]]):
        """
        Public method used to configure sorting results
        :param sort_by: Tuple of property enum to sort by and enum representing sorting order
            - SortOrder.ASC (ascending) or SortOrder.DESC (descending)
        """
        self.parser.parse_sort_by(*sort_by)
        return self

    def group_by(
        self,
        group_by: Union[PropEnum, str],
        group_ranges: Optional[Dict[str, List[PropValue]]] = None,
        include_ungrouped_results: bool = False,
    ):
        """
        Public method used to configure how to group results.
        :param group_by: Enum or string alias of the property to group by
        :param group_ranges: a set of optional group mappings - group name to list of values of
        selected group by property to be included in each group
        :param include_ungrouped_results: an optional flag to include a "ungrouped" group to the
        output of values found that were
        not specified in group mappings - ignored if group ranges not given
        """
        self.parser.parse_group_by(group_by, group_ranges, include_ungrouped_results)
        return self

    def run(
        self,
        cloud_account: str = None,
        from_subset: Optional[List[OpenstackResourceObj]] = None,
        **kwargs,
    ):
        """
        Public method that runs the query provided and outputs
        :param cloud_account: A String for the clouds configuration to use
        :param from_subset: A subset of openstack resources to run query on instead of querying openstacksdk
        :param kwargs: keyword args that can be used to configure details of how query is run
            - valid kwargs specific to resource
        """
        if not cloud_account and not from_subset:
            raise ParseQueryError(
                "please provide as a parameter, one of:"
                "\n\tcloud_account - a cloud domain to run query using openstacksdk"
                "\n\tfrom_subset - a set of openstack objects"
            )

        if from_subset:
            filters = (
                self.builder.client_side_filters + self.builder.server_filter_fallback
            )
            self.executor.run_with_subset(
                subset=from_subset, client_side_filters=filters
            )
        else:
            self.executor.run_with_openstacksdk(
                cloud_account=cloud_account,
                client_side_filters=self.builder.client_side_filters,
                server_side_filters=self.builder.server_side_filters,
                **kwargs,
            )

        link_prop, forwarded_vals = self.chainer.forwarded_info
        if forwarded_vals:
            self.executor.apply_forwarded_results(
                link_prop,
                deepcopy(forwarded_vals),
            )

        self.results_container = self.executor.results_container
        return self

    def to_objects(
        self, groups: Optional[List[str]] = None
    ) -> Union[Dict[str, List], List]:
        """
        Public method to return results as openstack objects.
        This is either returned as a list if no groups are specified, or as a dict if they grouping was requested
        :param groups: a list of group keys to limit output by
        """
        if self.executor.has_forwarded_results:
            logger.warning(
                "This Query has properties from previous queries. Running to_objects WILL IGNORE THIS "
                "Use to_props() instead if you want to include these properties"
            )

        self.results_container.parse_results(self.parser.run_parser)
        return self.output.to_objects(self.results_container, groups)

    def to_props(
        self, flatten: bool = False, groups: Optional[List[str]] = None
    ) -> Union[Dict[str, List], List]:
        """
        Public method to return results as openstack properties.
        This is either returned as a list if no groups are specified, or as a dict if they grouping was requested
        :param flatten: boolean which will flatten results if true
        :param groups: a list of group keys to limit output by
        """
        self.results_container.parse_results(self.parser.run_parser)
        return self.output.to_props(self.results_container, flatten, groups)

    def to_string(
        self,
        title: Optional[str] = None,
        groups: Optional[List[str]] = None,
        include_group_titles: bool = True,
        **kwargs,
    ) -> str:
        """
        Public method to return results as table(s)
        :param title: an optional title for the table(s)
        :param groups: a list group to limit output by
        :param include_group_titles: include group name as subtitle when printing groups
        :param kwargs: kwargs to pass to generate table
        """
        self.results_container.parse_results(self.parser.run_parser)
        return self.output.to_string(
            self.results_container, title, groups, include_group_titles, **kwargs
        )

    def to_html(
        self,
        title: Optional[str] = None,
        groups: Optional[List[str]] = None,
        include_group_titles: bool = True,
        **kwargs,
    ) -> str:
        """
        Public method to return results as html table
        :param title: an optional title for the table(s) - will be converted to html automatically
        :param groups: a list group to limit output by
        :param include_group_titles: include group name as subtitle when printing groups
        :param kwargs: kwargs to pass to generate table
        """
        self.results_container.parse_results(self.parser.run_parser)
        return self.output.to_html(
            self.results_container, title, groups, include_group_titles, **kwargs
        )

    def to_csv(
        self,
        groups: Optional[List[str]] = None,
        flatten_groups: bool = False,
    ) -> str:
        """
        Public method to return results as csv string.
        :param groups: a list of groups to limit output by
        :param flatten_groups: If True, grouped data is merged into a single CSV with a 'group' column.
        """
        self.results_container.parse_results(self.parser.run_parser)
        return self.output.to_csv(self.results_container, groups, flatten_groups)

    def to_json(
        self,
        groups: Optional[List[str]] = None,
        flatten_groups: bool = False,
        pretty: bool = False,
    ) -> str:
        """
        Public method to return results as a json string.
        :param groups: optional list of group keys to limit output by.
        :param flatten_groups: if True and results are grouped, merge all groups into a single list with group info.
        :param pretty: if True, return pretty-printed JSON.
        """
        self.results_container.parse_results(self.parser.run_parser)
        return self.output.to_json(
            self.results_container, groups, flatten_groups, pretty
        )

    def then(
        self, query_type: Union[str, "QueryTypes"], keep_previous_results: bool = True
    ):
        """
        Public method to chain current query into another query of a different type
        and return the new query so that it will work only on the results of the original query.
        NOTE - query must be run first for this to work
        NOTE - a shared common property must exist between this query and the new query
            - i.e. both ServerQuery and UserQuery share the 'USER_ID' property so chaining is possible
                - see Mappings for more chaining options

        :param query_type: an enum representing the new query to chain into
        :param keep_previous_results:
            - If True - will forward outputs from this query (and previous chained queries) onto new query.
            - If False - runs the query based on the previous results as a filter without adding additional fields
            NOTE: You will NOT be able to group/sort by these properties in the new query
        """
        return self.chainer.parse_then(self, query_type, keep_previous_results)

    def append_from(
        self,
        query_type: Union[str, "QueryTypes"],
        cloud_account: str,
        props: List[PropEnum],
    ):
        """
        Public method to append specific properties from other queries to the output
        of this query. This method will run a secondary query on top of this one to get required properties
        and append the properties to the results of this query
        NOTE - query must be run first for this to work
        NOTE - a shared common property must exist between this query and the new query
            - i.e. both ServerQuery and UserQuery share the 'USER_ID' property so chaining is possible
                - see Mappings for more chaining options

        :param query_type: an enum representing the new query to chain into
        :param cloud_account: A string for the clouds configuration to use
        :param props: list of props from new queries to get
        """
        link_prop, results = self.chainer.run_append_from_query(
            self, query_type, cloud_account, props
        )
        self.results_container.apply_forwarded_results(link_prop, results)
        return self
