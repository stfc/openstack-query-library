from enum import auto
from openstackquery.enums.enum_with_aliases import EnumWithAliases

# pylint: disable=too-few-public-methods


class QueryPresets(EnumWithAliases):
    """
    Enum class which holds generic query comparison operators
    """

    # generic comparisons
    EQUAL_TO = auto()
    NOT_EQUAL_TO = auto()
    ANY_IN = auto()
    NOT_ANY_IN = auto()

    # integer comparisons
    GREATER_THAN = auto()
    GREATER_THAN_OR_EQUAL_TO = auto()
    LESS_THAN = auto()
    LESS_THAN_OR_EQUAL_TO = auto()

    # datetime comparisons
    OLDER_THAN = auto()
    OLDER_THAN_OR_EQUAL_TO = auto()
    YOUNGER_THAN = auto()
    YOUNGER_THAN_OR_EQUAL_TO = auto()

    # string comparisons
    MATCHES_REGEX = auto()

    # list comparisons
    CONTAINS = auto()
    NOT_CONTAINS = auto()

    @staticmethod
    def _get_aliases():
        """
        A method that returns all valid string alias mappings
        """
        return {
            QueryPresets.EQUAL_TO: ["equal", "=="],
            QueryPresets.NOT_EQUAL_TO: ["not_equal", "!="],
            QueryPresets.ANY_IN: ["in"],
            QueryPresets.NOT_ANY_IN: ["not_in"],
            QueryPresets.LESS_THAN: ["less", "<"],
            QueryPresets.GREATER_THAN: ["greater", "more_than", "more", ">"],
            QueryPresets.GREATER_THAN_OR_EQUAL_TO: [
                "greater_or_equal",
                "more_than_or_equal_to",
                "more_or_equal",
                ">=",
            ],
            QueryPresets.LESS_THAN_OR_EQUAL_TO: ["less_or_equal", "<="],
            QueryPresets.YOUNGER_THAN: ["younger", "newer_than", "newer"],
            QueryPresets.OLDER_THAN: ["older"],
            QueryPresets.OLDER_THAN_OR_EQUAL_TO: ["older_or_equal"],
            QueryPresets.YOUNGER_THAN_OR_EQUAL_TO: [
                "younger_or_equal",
                "newer_than_or_equal_to",
                "newer_or_equal",
                "<=",
            ],
            QueryPresets.MATCHES_REGEX: ["match_regex", "regex", "re"],
            # QueryPresets.CONTAINS: ["list_contains", "has"],
            # QueryPresets.NOT_CONTAINS: ["list_not_contains", "has_not"]
        }
