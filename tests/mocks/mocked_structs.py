from openstackquery.structs.query_preset_details import QueryPresetDetails
from openstackquery.structs.query_output_details import QueryOutputDetails

from openstackquery.enums.query_output_types import QueryOutputTypes

from tests.mocks.mocked_props import MockProperties
from tests.mocks.mocked_query_presets import MockQueryPresets

# Mocked Preset Details Dataclass object - which uses mocked Prop and Preset Enums
MOCKED_PRESET_DETAILS = QueryPresetDetails(
    preset=MockQueryPresets.ITEM_1,
    prop=MockProperties.PROP_1,
    args={"arg1": "val1", "arg2": "val2"},
)

# Mocked Output Details Dataclass object - which uses mocked Prop and Preset Enums
MOCKED_OUTPUT_DETAILS = QueryOutputDetails(
    properties_to_select=[MockProperties.PROP_1, MockProperties.PROP_2],
    output_type=QueryOutputTypes.TO_STR,
)

MOCKED_OUTPUT_DETAILS_TO_OBJ_LIST = QueryOutputDetails(
    output_type=QueryOutputTypes.TO_OBJECT_LIST,
    # should be ignored
    properties_to_select=[MockProperties.PROP_1, MockProperties.PROP_2],
)

MOCKED_OUTPUT_DETAILS_WITH_GROUP_BY = QueryOutputDetails(
    properties_to_select=[MockProperties.PROP_1, MockProperties.PROP_2],
    output_type=QueryOutputTypes.TO_STR,
    group_by=MockProperties.PROP_1,
    group_ranges={"group1": ["val1"], "group2": ["val2"]},
    include_ungrouped_results=True,
)

MOCKED_OUTPUT_DETAILS_WITH_SORT_BY = QueryOutputDetails(
    properties_to_select=[MockProperties.PROP_1, MockProperties.PROP_2],
    output_type=QueryOutputTypes.TO_STR,
    sort_by=[(MockProperties.PROP_1, False), (MockProperties.PROP_2, True)],
)

MOCKED_OUTPUT_DETAILS_WITH_ALL = QueryOutputDetails(
    properties_to_select=[MockProperties.PROP_1, MockProperties.PROP_2],
    output_type=QueryOutputTypes.TO_STR,
    group_by=MockProperties.PROP_1,
    group_ranges={"group1": ["val1"], "group2": ["val2"]},
    include_ungrouped_results=True,
    sort_by=[(MockProperties.PROP_1, False), (MockProperties.PROP_2, True)],
)
