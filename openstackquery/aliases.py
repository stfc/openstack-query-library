from typing import List, Callable, Any, Dict, Union, Literal
from openstack.identity.v3.project import Project

from openstackquery.enums.props.prop_enum import PropEnum
from openstackquery.enums.query_presets import QueryPresets


PropValue = Union[str, bool, int, None]

# A type alias for a single openstack resource - i.e Server, Hypervisor etc
OpenstackResourceObj = Any

# A type alias for a function which takes an openstack resource and returns it's value for a given property
PropFunc = Callable[[OpenstackResourceObj], PropValue]

# A type alias which maps a property enum to the function that returns it
PropertyMappings = Dict[PropEnum, PropFunc]

# A type alias for storing the input parameters for handling query filtering (filter name -> value(s))
FilterParams = Dict[str, Union[PropValue, List[PropValue]]]

# type alias for a generic filter function - takes a value to compare and parameters to define the filter conditions
#   - returns True if a given property value matches filter condition
#   - returns False if not
FilterFunc = Callable[[PropValue, Any], bool]

# A type alias for a client-side filter function. Wraps a generic filter function
#   - takes a openstack resource object
#   - extracts desired property
#   - applies stored generic filter function - see FilterFunc
ClientSideFilterFunc = Callable[[OpenstackResourceObj], bool]

# A list of client-side filter functions that make up a single query
#   - applied after querying openstacksdk
#   - applied sequentially - act as logical "AND" filters
ClientSideFilters = List[ClientSideFilterFunc]

# A type alias for a server-side filter.
#   - kwargs to pass to openstacksdk which handles filtering for us
#   - faster than using client-side filters
ServerSideFilter = Dict[str, PropValue]

# A list of server-side filters
# each set of filters create a separate queries - results of which are aggregated together
ServerSideFilters = List[ServerSideFilter]

# A type alias for a function that:
# - takes a set of filter params as input
# - returns kwargs to pass to openstacksdk to apply filter
ServerSideFilterFunc = Callable[[FilterParams], ServerSideFilter]

# A type alias for mapping preset/property pairs to corresponding server-side filter functions
# Each QueryPreset contains a set of property enums that are valid for the preset
# Each enum is mapped to a filter function that returns server-side kwargs to pass to openstacksdk
ServerSideFilterMappings = Dict[QueryPresets, Dict[PropEnum, ServerSideFilterFunc]]

# A type alias for mapping client-side query presets to the properties they act on
# Maps a preset to list of valid property enums
# - accepts ['*'] - indicates all PropEnums are valid
# - or accepts a list of valid PropEnums
ClientSidePresetPropertyMappings = Dict[
    QueryPresets, Union[List[Literal["*"]], List[PropEnum]]
]

# type alias for mapping preset to a filter function
# client-side filters are more generic than server-side filters
# - every valid property for a preset uses the same filter function
ClientSideFilterMappings = Dict[QueryPresets, FilterFunc]

# type alias for project identifier - either name/id or Project object
ProjectIdentifier = Union[str, Project]

# type alias for returning a query - any one of:
#   - A string with values in a tabulate table
#   - A list of Openstack Resource objects
#   - A list of dictionaries containing selected properties for each openstack resource
QueryReturn = Union[str, List[OpenstackResourceObj], List[Dict]]

# type alias for group mappings, a dictionary with group name as keys mapped to a function which takes
# an openstack resource object and returns a True if resource belongs to that group, False if not
GroupMappings = Dict[str, Callable[[OpenstackResourceObj], bool]]

# type alias for group ranges, a dictionary with group name as keys mapped to a list of prop values
# that should belong to that group
GroupRanges = Dict[str, List[PropValue]]

# a type alias for grouped and parsed outputs. A dicitonary of grouped prop-value as key and list of values
# that belong to that group
GroupedReturn = Dict[PropValue, List[Dict]]
