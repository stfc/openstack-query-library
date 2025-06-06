import csv
import io
import json
from typing import Dict, List, Optional, Set, Type, Union

from tabulate import tabulate

from openstackquery.aliases import PropValue
from openstackquery.enums.props.prop_enum import PropEnum
from openstackquery.exceptions.parse_query_error import ParseQueryError
from openstackquery.query_blocks.results_container import ResultsContainer


class QueryOutput:
    """
    Helper class for generating output for the query as a formatted table or selected properties - either as
    html or string

    TODO: Class should also handle grouping and sorting results
    """

    # what value to output if property is not found for an openstack object
    DEFAULT_OUT = "Not Found"

    def __init__(self, prop_enum_cls: Type[PropEnum]):
        self._prop_enum_cls = prop_enum_cls
        self._props = set()

    @property
    def selected_props(self) -> List[PropEnum]:
        """
        A getter for selected properties relevant to the query
        """
        if not self._props:
            return []
        return list(self._props)

    @selected_props.setter
    def selected_props(self, props=Set[PropEnum]):
        """
        A setter for setting selected properties
        :param props: A set of property enums to select for
        """
        self._props = props

    @staticmethod
    def _validate_groups(
        results: Union[List, Dict], groups: Optional[List[str]] = None
    ):
        """
        helper method which takes a set of grouped results and a list of groups and
        outputs a subset of results where each key in subset matches a value in given set of groups.
        method will return all results if groups not given.
        Outputs error if:
            - groups contains a value not in results
            - given results aren't grouped
        :param results: results to get subset for if grouped and groups given
        :param groups: an optional list of keys to get a subset of results
        """
        if not groups:
            return results

        if not isinstance(results, dict):
            raise ParseQueryError(
                f"Result is not grouped - cannot filter by given group(s) {groups}"
            )
        if not all(group in results.keys() for group in groups):
            raise ParseQueryError(
                f"Group(s) given are invalid - valid groups {list(results.keys())}"
            )
        return {group_key: results[group_key] for group_key in groups}

    def to_objects(
        self, results_container: ResultsContainer, groups: Optional[List[str]] = None
    ) -> Union[Dict[str, List], List]:
        """
        return results as openstack objects
        :param results_container: container object which stores results
        :param groups: a list of group keys to limit output by

        """
        results = results_container.to_objects()
        return self._validate_groups(results, groups)

    def to_props(
        self,
        results_container: ResultsContainer,
        flatten: bool = False,
        groups: Optional[List[str]] = None,
    ) -> Union[Dict[str, List], List]:
        """
        return results as selected props
        :param results_container: container object which stores results
        :param flatten: boolean which will flatten results if true
        :param groups: a list of group keys to limit output by
        """
        results = results_container.to_props(*self.selected_props)
        results = self._validate_groups(results, groups)
        if flatten:
            results = self._flatten(results)
        return results

    def to_string(
        self,
        results_container: ResultsContainer,
        title: Optional[str] = None,
        groups: Optional[List[str]] = None,
        include_group_titles: [bool] = True,
        **kwargs,
    ):
        """
        return results as a table of selected properties
        :param results_container: container object which stores results
        :param title: an optional title for the table when it gets outputted
        :param groups: a list of groups to limit output by
        :param include_group_titles: include group name as subtitle when printing groups
        :param kwargs: kwargs to pass to _generate_table method
        """
        results = results_container.to_props(*self.selected_props)
        results = self._validate_groups(results, groups)

        output = "" if not title else f"{title}:\n"

        if isinstance(results, dict):
            for group_title in list(results.keys()):
                output += self._generate_table(
                    results[group_title],
                    return_html=False,
                    title=f"{group_title}:\n" if include_group_titles else None,
                    **kwargs,
                )
                output += "\n\n"
        else:
            output += self._generate_table(
                results, return_html=False, title=None, **kwargs
            )
            output += "\n\n"
        return output

    def to_html(
        self,
        results_container: ResultsContainer,
        title: str = None,
        groups: Optional[List[str]] = None,
        include_group_titles: bool = True,
        **kwargs,
    ) -> str:
        """
        method to return results as html table
        :param results_container: container object which stores results
        :param title: a title for the table(s) when it gets outputted
        :param groups: a list of groups to limit output by
        :param include_group_titles: include group name as subtitle when printing groups
        :param kwargs: kwargs to pass to generate table
        """
        results = results_container.to_props(*self.selected_props)
        results = self._validate_groups(results, groups)
        output = "" if not title else f"<b>{title}:</b><br/>"

        if isinstance(results, dict):
            for group_title in list(results.keys()):
                output += self._generate_table(
                    results[group_title],
                    return_html=True,
                    title=(
                        f"<b>{group_title}:</b><br/>" if include_group_titles else None
                    ),
                    **kwargs,
                )
                output += "<br/><br/>"
        else:
            output += self._generate_table(
                results, return_html=True, title=None, **kwargs
            )
            output += "<br/><br/>"
        return output

    def _parse_select_inputs(self, props):
        """
        Converts list of select() 'prop' user inputs into Enums, any string aliases will be converted into Enums
        :param props: one or more Enums/string aliases representing properties to show
        """
        parsed_props = []
        for prop in props:
            if isinstance(prop, str):
                prop = self._prop_enum_cls.from_string(prop)
            parsed_props.append(prop)
        return parsed_props

    def parse_select(self, *props: Union[str, PropEnum], select_all=False) -> None:
        """
        Method which is used to set which properties to output once results are gathered
        This method checks that each Enum provided is valid and populates internal attribute which holds selected props
        :param select_all: boolean flag to select all valid properties
        :param props: one or more Enums/string aliases representing properties to show
        """
        if select_all:
            self.selected_props = set(self._prop_enum_cls)
            return

        props = self._parse_select_inputs(props)
        all_props = set()
        for prop in props:
            if prop not in self._prop_enum_cls:
                raise ParseQueryError(
                    f"Error: Given property to select: {prop.name} is not supported by query"
                )
            all_props.add(prop)

        self.selected_props = set(all_props)

    @staticmethod
    def _generate_table(
        results: List[Dict[str, PropValue]], return_html: bool, title=None, **kwargs
    ) -> str:
        """
        Returns a table from the result of 'self.parse_properties'
        :param results: dict of query results
        :param return_html: True if output required in html table format else output plain text table
        :param kwargs: kwargs to pass to tabulate
        :return: String (html or plaintext table of results)
        """
        output = "" if not title else f"{title}"

        if results:
            headers = list(results[0].keys())
            rows = [list(row.values()) for row in results]
            output += tabulate(
                rows, headers, tablefmt="html" if return_html else "grid", **kwargs
            )
        else:
            output += "No results found"
        return output

    @staticmethod
    def _flatten(data: Union[List, Dict]) -> Optional[Dict]:
        """
        Utility function for flattening output to instead get list of unique
        values found for each property selected. results will also be grouped if given
        data is grouped too
        :param data: output to flatten
        """
        if not data:
            return None

        if isinstance(data, list):
            return QueryOutput._flatten_list(data)

        result = {}
        for group_key, values in data.items():
            result[group_key] = QueryOutput._flatten_list(values)

        return result

    @staticmethod
    def _flatten_list(data: List[Dict]) -> Dict:
        """
        Helper function to flatten a query output list. This will return
        a dictionary where the keys are strings representing the property and
        the value is a list of unique values found in the given output list for that property.
        Output list can be actual query output (if it's a list) or one group of grouped results
        :param data: output list to flatten
        """
        if not data:
            return {}

        keys = list(data[0].keys())
        res = {}
        for key in keys:
            res[key] = [d[key] for d in data]
        return res

    @staticmethod
    def _convert_to_csv_string(data: Union[List, Dict]) -> str:
        output = io.StringIO()
        if not data or not (len(data) > 0 and data[0].keys()):
            raise RuntimeError(
                "Error: Could not write to csv: No results found, or no properties selected to output"
            )
        fields = data[0].keys()
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue().strip()

    def to_csv(
        self,
        results_container: ResultsContainer,
        groups: Optional[List[str]] = None,
        flatten_groups: bool = False,
    ) -> str:
        """
        Method to return results as csv string, with headers if grouped.
        Optionally creates files at a given path, in seperate files if grouped.
        :param results_container: container object which stores results.
        :param groups: a list of groups to limit output by
        :param flatten_groups: If True, grouped data is merged into a single CSV with a 'group' column.
        """
        results = results_container.to_props(*self.selected_props)
        results = self._validate_groups(results, groups)

        if flatten_groups and isinstance(results, dict):
            merged_list = []
            for group, items in results.items():
                for item in items:
                    item_with_group = dict(item)
                    item_with_group["group"] = group
                    merged_list.append(item_with_group)
            results = merged_list

        if isinstance(results, dict):
            csv_chunks = []
            for group, items in results.items():
                csv_chunk = f"# Group: {group}\n" + self._convert_to_csv_string(items)
                csv_chunks.append(csv_chunk)
            return "\n\n".join(csv_chunks)

        return self._convert_to_csv_string(results)

    def to_json(
        self,
        results_container: ResultsContainer,
        groups: Optional[List[str]] = None,
        flatten_groups: bool = False,
        pretty: bool = False,
    ) -> str:
        """
        Method to return results as a JSON string.
        :param results_container: container object which stores results.
        :param groups: optional list of group keys to limit output by.
        :param flatten_groups: if True and results are grouped, merge all groups into a single list with group info.
        :param pretty: if True, return pretty-printed JSON.
        :return: JSON string representation of results.
        """
        results = results_container.to_props(*self.selected_props)
        results = self._validate_groups(results, groups)

        if flatten_groups and isinstance(results, dict):
            merged_list = []
            for group, items in results.items():
                for item in items:
                    item_with_group = dict(item)
                    item_with_group["group"] = group
                    merged_list.append(item_with_group)
            results = merged_list

        if pretty:
            return json.dumps(results, indent=4)

        return json.dumps(results)
