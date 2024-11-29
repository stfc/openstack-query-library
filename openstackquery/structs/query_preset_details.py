from typing import Any, Dict
from dataclasses import dataclass

from openstackquery.enums.props.prop_enum import PropEnum
from openstackquery.enums.query_presets import QueryPresets


@dataclass
class QueryPresetDetails:
    """
    Structured data passed to a Query<Resource> object when calling the where() function
    describes how to filter for the query.
    """

    preset: QueryPresets
    prop: PropEnum
    args: Dict[str, Any]
