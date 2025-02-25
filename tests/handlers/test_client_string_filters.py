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
    Returns True if test_prop matches given regex pattern regex_string
    """
    assert (
        run_client_filter_test(
            QueryPresets.MATCHES_REGEX, test_prop, {"value": regex_string}
        )
        == expected
    )
