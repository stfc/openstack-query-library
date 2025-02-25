import pytest
from openstackquery.enums.query_presets import QueryPresets


@pytest.mark.parametrize(
    "prop_list,values,expected",
    [
        # Single value tests
        ([1, 2, 3], 2, True),  # Value in list
        ([1, 2, 3], 4, False),  # Value not in list
        (["a", "b", "c"], "b", True),  # String value in list
        (["a", "b", "c"], "d", False),  # String value not in list
        # Sublist tests
        ([1, 2, 3, 4], [1, 3], True),  # All values from sublist in prop list
        ([1, 2, 3], [1, 4], False),  # Some values from sublist not in prop list
        (["a", "b", "c", "d"], ["a", "c"], True),  # String sublist all in prop list
        (["a", "b", "c"], ["a", "d"], False),  # String sublist partially in prop list
        # Edge cases
        ([1, 2, 3], [], True),  # Empty sublist (all() on empty is True)
        ([], [], True),  # Empty lists
        ([], 1, False),  # Empty prop list with value
        ([], [1, 2], False),  # Empty prop list with sublist
        (None, 1, False),  # None prop list with value
        (None, [1, 2], False),  # None prop list with sublist
        # Special cases
        ([1, 2, 2, 3], 2, True),  # Duplicate values in prop list
        ([1, 2, 2, 3], [2, 3], True),  # Sublist with duplicate in prop list
        ([1, "string", True], "string", True),  # Mixed types value
        ([1, "string", True], [1, True], True),  # Mixed types sublist
    ],
)
def test_prop_list_contains(prop_list, values, expected, run_client_filter_test):
    """Test prop_list_contains function with various inputs"""
    assert (
        run_client_filter_test(QueryPresets.CONTAINS, prop_list, {"values": values})
        == expected
    )


# Test cases for prop_list_not_contains
@pytest.mark.parametrize(
    "prop_list, values, expected",
    [
        # Single value tests
        ([1, 2, 3], 2, False),  # Value in list
        ([1, 2, 3], 4, True),  # Value not in list
        (["a", "b", "c"], "b", False),  # String value in list
        (["a", "b", "c"], "d", True),  # String value not in list
        # Sublist tests
        ([1, 2, 3, 4], [1, 3], False),  # All values from sublist in prop list
        ([1, 2, 3], [1, 4], True),  # Some values from sublist not in prop list
        (["a", "b", "c", "d"], ["a", "c"], False),  # String sublist all in prop list
        (["a", "b", "c"], ["a", "d"], True),  # String sublist partially in prop list
        # Edge cases
        ([1, 2, 3], [], False),  # Empty sublist
        ([], [], False),  # Empty lists
        ([], 1, True),  # Empty prop list with value
        ([], [1, 2], True),  # Empty prop list with sublist
        (None, 1, True),  # None prop list with value
        (None, [1, 2], True),  # None prop list with sublist
        # Special cases
        ([1, 2, 2, 3], 2, False),  # Duplicate values in prop list
        ([1, 2, 2, 3], [2, 3], False),  # Sublist with duplicate in prop list
        ([1, "string", True], "string", False),  # Mixed types value
        ([1, "string", True], [1, True], False),  # Mixed types sublist
    ],
)
def test_prop_list_not_contains(prop_list, values, expected, run_client_filter_test):
    """Test prop_list_not_contains function with various inputs"""
    assert (
        run_client_filter_test(QueryPresets.NOT_CONTAINS, prop_list, {"values": values})
        == expected
    )
