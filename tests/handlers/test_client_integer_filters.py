from openstackquery.enums.query_presets import QueryPresets


def test_prop_less_than(run_client_filter_test):
    """
    Tests that method prop_less_than functions expectedly
    Returns True if val1 is less than val2
    """
    for i, expected in (1, True), (2, False):
        assert (
            run_client_filter_test(QueryPresets.LESS_THAN, i, {"value": 2}) == expected
        )


def test_prop_greater_than(run_client_filter_test):
    """
    Tests that method prop_greater_than functions expectedly
    Returns True if val1 is greater than val2
    """
    for i, expected in (1, False), (2, False), (3, True):
        assert (
            run_client_filter_test(QueryPresets.GREATER_THAN, i, {"value": 2})
            == expected
        )


def test_prop_less_than_or_equal_to(run_client_filter_test):
    """
    Tests that method prop_less_than_or_equal_to functions expectedly
    Returns True if val1 is less than or equal to val2
    """
    for i, expected in (1, True), (2, True), (3, False):
        assert (
            run_client_filter_test(QueryPresets.LESS_THAN_OR_EQUAL_TO, i, {"value": 2})
            == expected
        )


def test_prop_greater_than_or_equal_to(run_client_filter_test):
    """
    Tests that method prop_greater_than_or_equal_to functions expectedly
    Returns True if val1 is greater than or equal to val2
    """
    for i, expected in (1, False), (2, True), (3, True):
        assert (
            run_client_filter_test(
                QueryPresets.GREATER_THAN_OR_EQUAL_TO, i, {"value": 2}
            )
            == expected
        )
