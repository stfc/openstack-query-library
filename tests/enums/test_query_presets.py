import pytest

from openstackquery.enums.query_presets import QueryPresets
from openstackquery.exceptions.parse_query_error import ParseQueryError


@pytest.mark.parametrize(
    "expected_prop,test_values",
    [
        (QueryPresets.EQUAL_TO, ["equal_to", "equal", "=="]),
        (QueryPresets.NOT_EQUAL_TO, ["not_equal_to", "not_equal", "!="]),
        (
            QueryPresets.GREATER_THAN,
            ["greater_than", "greater", "more_than", "more", ">"],
        ),
        (
            QueryPresets.GREATER_THAN_OR_EQUAL_TO,
            [
                "greater_than_or_equal_to",
                "greater_or_equal",
                "more_than_or_equal_to",
                "more_or_equal",
                ">=",
            ],
        ),
        (QueryPresets.LESS_THAN, ["less_than", "less", "<"]),
        (
            QueryPresets.LESS_THAN_OR_EQUAL_TO,
            ["less_than_or_equal_to", "less_or_equal", "<="],
        ),
        (QueryPresets.OLDER_THAN, ["older_than", "older"]),
        (
            QueryPresets.OLDER_THAN_OR_EQUAL_TO,
            ["older_than_or_equal_to", "older_or_equal"],
        ),
        (QueryPresets.YOUNGER_THAN, ["younger_than", "younger", "newer_than", "newer"]),
        (
            QueryPresets.YOUNGER_THAN_OR_EQUAL_TO,
            [
                "younger_than_or_equal_to",
                "younger_or_equal",
                "newer_than_or_equal_to",
                "newer_or_equal",
            ],
        ),
        (QueryPresets.ANY_IN, ["any_in", "in"]),
        (QueryPresets.NOT_ANY_IN, ["not_any_in", "not_in"]),
        (QueryPresets.MATCHES_REGEX, ["matches_regex", "match_regex", "regex", "re"]),
    ],
)
def test_query_presets_serialization(
    expected_prop, test_values, property_variant_generator
):
    """Test all query preset name formats can be correctly serialized."""
    for variant in property_variant_generator(test_values):
        assert QueryPresets.from_string(variant) is expected_prop


def test_get_preset_from_string_invalid():
    """
    Tests that get_preset_from_string returns error if given an invalid alias
    """
    with pytest.raises(ParseQueryError):
        QueryPresets.from_string("invalid-alias")
