from datetime import datetime, timedelta
import re
from typing import Optional


class TimeUtils:
    @staticmethod
    def get_timestamp_in_seconds(
        days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0
    ) -> float:
        """
        Function which takes a number of days, hours, minutes, and seconds - and calculates the total seconds
        :param days: (Optional) number of days
        :param hours: (Optional) number of hours
        :param minutes: (Optional) number of minutes
        :param seconds: (Optional) number of seconds
        """
        if all(arg == 0 for arg in [days, hours, minutes, seconds]):
            raise RuntimeError(
                "requires at least 1 argument for function to be non-zero"
            )

        current_time = datetime.now().timestamp()
        prop_time_in_seconds = timedelta(
            days=days, hours=hours, minutes=minutes, seconds=float(seconds)
        ).total_seconds()

        return current_time - prop_time_in_seconds

    @staticmethod
    def convert_to_timestamp(
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
    ) -> str:
        """
        Helper function to convert a relative time from current time into a timestamp
        :param days: (Optional) relative number of days since current time
        :param hours: (Optional) relative number of hours since current time
        :param minutes: (Optional) relative number of minutes since current time
        :param seconds: (Optional) relative number of seconds since current time
        """

        time_in_seconds = timedelta(
            days=days, hours=hours, minutes=minutes, seconds=float(seconds)
        ).total_seconds()
        current_time = datetime.now().timestamp()
        return datetime.fromtimestamp(current_time - time_in_seconds).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )

    @staticmethod
    def extract_uptime(uptime_string: str) -> Optional[float]:
        """
        Extracts number of days uptime from the string returned by the uptime
        command

        :param uptime_string: String returned by the uptime command
        :type uptime_string: str
        :return: Number of days uptime if found in string
        :rtype: float | None
        """
        uptime_pattern = re.compile(r"up\s+((\d+ days?,\s*)?(\d+:\d+))")
        try:
            match = uptime_pattern.search(uptime_string)
        except TypeError:
            return None
        if match:
            uptime_string = match.group(1)
            days = 0
            if "days" in uptime_string:
                days_part, time_part = uptime_string.split(" days, ")
                days += int(days_part)
            else:
                time_part = uptime_string

            hours, minutes = map(int, time_part.split(":"))
            days += hours / 24 + minutes / 1440
            return round(days, 2)
        return None
