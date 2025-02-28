from unittest.mock import patch, NonCallableMock, MagicMock, call
import pytest

from openstackquery.enums.query_presets import QueryPresets
from tests.mocks.mocked_props import MockProperties


@pytest.fixture(name="run_client_dt_filter_test")
def run_client_dt_filter_test_fixture(filter_test_instance):
    """
    fixture to run a test cases for each client-side filter function
    """

    @patch("openstackquery.time_utils.TimeUtils.get_timestamp_in_seconds")
    @patch("openstackquery.handlers.client_side_filters.datetime")
    def _run_client_dt_filter_test(
        preset, prop_value, mock_current_time, mock_datetime, mock_get_timestamp
    ):
        """
        runs a test case by calling get_filter_func for datetime related filters
        with a given preset, prop return value and value to compare against.
        :param preset: preset (mapped to filter func we want to test)
        :param prop_value: property value to test filter func with
        :param mock_current_time: mock value for current timestamp
        :param mock_datetime: mock datetime object
        :param mock_get_timestamp: mock get_timestamp_in_seconds function
        """

        # we mock and set the timestamp return values manually since it's difficult testing datetime
        mock_datetime.strptime.return_value.timestamp.return_value = prop_value
        mock_get_timestamp.return_value = mock_current_time

        # mock the kwargs - they won't be used
        days, hours, mins, secs = (
            NonCallableMock(),
            NonCallableMock(),
            NonCallableMock(),
            NonCallableMock(),
        )
        mock_kwargs = {"days": days, "hours": hours, "minutes": mins, "seconds": secs}

        prop_func = MagicMock()
        filter_func = filter_test_instance.get_filter_func(
            preset, MockProperties.PROP_1, prop_func, mock_kwargs
        )

        mock_obj = NonCallableMock()
        res = filter_func(mock_obj)

        prop_func.assert_called_once_with(mock_obj)
        mock_datetime.strptime.assert_has_calls(
            [call(prop_func.return_value, "%Y-%m-%dT%H:%M:%SZ"), call().timestamp()]
        )
        mock_get_timestamp.assert_called_once_with(days, hours, mins, secs)

        return res

    return _run_client_dt_filter_test


def test_prop_older_than(run_client_dt_filter_test):
    """
    Tests prop_older_than client-side-filter with different values
    This essentially compares two numbers (number of seconds) and if the prop value is lower, it returns True
    because older timestamps have fewer seconds passed since 1970 than newer ones
    """
    for i, expected in [(200, False), (400, True), (300, False)]:
        assert run_client_dt_filter_test(QueryPresets.OLDER_THAN, 300, i) == expected


def test_prop_younger_than(run_client_dt_filter_test):
    """
    Tests younger_than client-side-filter with different values
    This essentially compares two numbers (number of seconds) and if the prop value is lower, it returns True
    because newer timestamps have more seconds passed since 1970 than older ones
    """
    for i, expected in [(200, True), (400, False), (300, False)]:
        assert run_client_dt_filter_test(QueryPresets.YOUNGER_THAN, 300, i) == expected


def test_prop_younger_than_or_equal_to(run_client_dt_filter_test):
    """
    Tests prop_younger_than_or_equal_to client-side-filter with different values
    Same as prop_younger_than, but if equal will also return True
    """
    for i, expected in [(200, True), (400, False), (300, True)]:
        assert (
            run_client_dt_filter_test(QueryPresets.YOUNGER_THAN_OR_EQUAL_TO, 300, i)
            == expected
        )


def test_prop_older_than_or_equal_to(run_client_dt_filter_test):
    """
    Tests prop_older_than_or_equal_to client-side-filter with different values
    Same as prop_older_than, but if equal will also return True
    """
    for i, expected in [(200, False), (400, True), (300, True)]:
        assert (
            run_client_dt_filter_test(QueryPresets.OLDER_THAN_OR_EQUAL_TO, 300, i)
            == expected
        )
