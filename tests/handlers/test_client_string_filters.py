from unittest.mock import patch

import pytest

from openstackquery.enums.query_presets import QueryPresets


@pytest.mark.parametrize(
    "regex_string, test_prop, expected",
    [
        # "Numeric digits only",
        ("[0-9]+", "123", True),
        # "Alphabetic characters only",
        ("[A-Za-z]+", "abc", True),
        # "No alphabetic characters",
        ("[A-Za-z]+", "123", False),
        # "Alphabetic and numeric characters",
        ("[A-Za-z0-9]+", "abc123", True),
        # "Empty string, no match",
        ("[0-9]+", "", False),
    ],
)
def test_prop_matches_regex(regex_string, test_prop, expected, run_client_filter_test):
    """
    Tests that method prop_matches_regex functions expectedly - with valid regex patterns
    Should return True if test_prop matches given regex pattern regex_string
    """
    assert (
        run_client_filter_test(
            QueryPresets.MATCHES_REGEX, test_prop, {"value": regex_string}
        )
        == expected
    )


@pytest.mark.parametrize(
    "regex_string, test_prop, expected",
    [
        # "Numeric digits only",
        ("[0-9]+", "123", False),
        # "Alphabetic characters only",
        ("[A-Za-z]+", "abc", False),
        # "No alphabetic characters",
        ("[A-Za-z]+", "123", True),
        # "Alphabetic and numeric characters",
        ("[A-Za-z0-9]+", "abc123", False),
        # "Empty string, no match",
        ("[0-9]+", "", True),
    ],
)
def test_prop_not_matches_regex(
    regex_string, test_prop, expected, run_client_filter_test
):
    """
    Tests that method prop_not_matches_regex functions expectedly - with valid regex patterns
    Should return True if test_prop does not match given regex pattern regex_string
    """
    with patch(
        "openstackquery.handlers.client_side_filters.prop_matches_regex"
    ) as regex_call:
        regex_call.return_value = not expected
        assert (
            run_client_filter_test(
                QueryPresets.NOT_MATCHES_REGEX, test_prop, {"value": regex_string}
            )
            == expected
        )
        # Cannot check called_once_with as _check_filter_func in the clientside handler calls with None as a test
        regex_call.assert_called_with(prop=test_prop, value=regex_string)
