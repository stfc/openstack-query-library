import pytest

from openstackquery.enums.sort_order import SortOrder
from openstackquery.exceptions.parse_query_error import ParseQueryError


@pytest.mark.parametrize(
    "expected_prop,test_values",
    [
        (SortOrder.ASC, ["asc", "ascending"]),
        (SortOrder.DESC, ["desc", "descending"]),
    ],
)
def test_sort_order_serialization(
    expected_prop, test_values, property_variant_generator
):
    """Test all sort order name formats can be correctly serialized."""
    for variant in property_variant_generator(test_values):
        assert SortOrder.from_string(variant) is expected_prop


def test_get_preset_from_string_invalid():
    """
    Tests that get_preset_from_string returns error if given an invalid alias
    """
    with pytest.raises(ParseQueryError):
        SortOrder.from_string("invalid-alias")
