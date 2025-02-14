from unittest.mock import patch
import pytest
from time_utils import TimeUtils


# pylint:disable=too-many-arguments
def test_get_timestamp_in_seconds():
    """
    Tests that get_timestamp_in_seconds method works expectedly
    method takes a set of integer params "days, hours, minutes, seconds" and calculates total seconds
    """
    days, hours, minutes, seconds = 1, 2, 3, 4

    with patch("time_utils.datetime") as mock_datetime:
        with patch("time_utils.timedelta") as mock_timedelta:
            mock_datetime.now.return_value.timestamp.return_value = 6
            mock_timedelta.return_value.total_seconds.return_value = 2
            out = TimeUtils.get_timestamp_in_seconds(days, hours, minutes, seconds)

    # Now - amount of time in the past = expected out
    assert out == 4

    mock_datetime.now.assert_called_once()
    mock_datetime.now.return_value.timestamp.assert_called_once()

    mock_timedelta.assert_called_once_with(
        days=days, hours=hours, minutes=minutes, seconds=float(seconds)
    )
    mock_timedelta.return_value.total_seconds.assert_called()


def test_get_timestamp_in_seconds_invalid():
    """
    Tests that get_timestamp_in_seconds method works expectedly - with invalid inputs - all 0
    method should raise an error - we should expect at least one non-zero param
    """
    with pytest.raises(RuntimeError):
        TimeUtils.get_timestamp_in_seconds(0, 0, 0, 0)


def test_convert_to_timestamp():
    """
    Tests that convert_to_timestamp method works expectedly
    method takes a set of integer params "days, hours, minutes, seconds" and calculates a relative timestamp
    of that many seconds in the past from current time
    """
    days, hours, minutes, seconds = 1, 2, 3, 4

    with patch("time_utils.datetime") as mock_datetime:
        with patch("time_utils.timedelta") as mock_timedelta:
            mock_datetime.now.return_value.timestamp.return_value = 6
            mock_timedelta.return_value.total_seconds.return_value = 2
            mock_datetime.fromtimestamp.return_value.strftime.return_value = (
                "timestamp-out"
            )
            out = TimeUtils.convert_to_timestamp(days, hours, minutes, seconds)

    mock_datetime.now.assert_called_once()
    mock_datetime.now.return_value.timestamp.assert_called_once()
    mock_timedelta.assert_called_once_with(
        days=days, hours=hours, minutes=minutes, seconds=float(seconds)
    )
    mock_timedelta.return_value.total_seconds.assert_called()
    mock_datetime.fromtimestamp.assert_called_once_with(6 - 2)
    mock_datetime.fromtimestamp.return_value.strftime.assert_called_once_with(
        "%Y-%m-%dT%H:%M:%SZ"
    )

    assert out == "timestamp-out"


def test_extract_uptime_not_string():
    """
    Test extraction returns None when not a string
    """
    assert TimeUtils.extract_uptime(None) is None


@pytest.mark.parametrize(
    "mock_string,expected_result",
    [
        # Test extraction when greater than a day
        (
            "17:13:49 up 394 days,  7:03,  0 users,  load average: 1.90, 1.70, 1.95",
            394.29,
        ),
        # Test extraction when HH:MM uptime format (less than a day)
        ("17:13:49 up  5:57,  0 users,  load average: 0.00, 0.01, 0.00", 0.25),
        # Test extraction when HH:MM uptime format (less than a day)
        ("17:13:49 up 1 day,  7:03,  0 users,  load average: 0.00, 0.01, 0.00", 1.29),
        # Test extraction when less than a hour uptime
        ("15:48:54 up 30 min,  1 user,  load average: 0.06, 0.39, 0.25", 0.02),
    ],
)
def test_extract_uptime(mock_string, expected_result):
    """
    Test extraction from empty string returns None
    """
    assert TimeUtils.extract_uptime(mock_string) == expected_result
