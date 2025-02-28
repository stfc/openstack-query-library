from typing import Union, Any, List
from datetime import datetime
import re

from openstackquery.time_utils import TimeUtils
from openstackquery.aliases import PropValue


def prop_older_than(
    prop: Union[str, None],
    days: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
):
    """
    Filter function which returns True if property older than a relative amount of time since current time.

    :param prop: prop value to check against - in UTC time
    :param days: (Optional) relative number of days since current time to compare against
    :param hours: (Optional) relative number of hours since current time to compare against
    :param minutes: (Optional) relative number of minutes since current time to compare against
    :param seconds: (Optional) relative number of seconds since current time to compare against

    By default, all time args are set to 0, i.e. now. Setting this to 10 seconds would mean 10 seconds in the past.
    You must give at least one non-zero argument (days, hours, minutes, seconds) otherwise a
    MissingMandatoryArgument exception will be thrown
    """
    if prop is None:
        return False
    prop_timestamp = datetime.strptime(prop, "%Y-%m-%dT%H:%M:%SZ").timestamp()
    given_timestamp = TimeUtils.get_timestamp_in_seconds(days, hours, minutes, seconds)

    return prop_timestamp < given_timestamp


def prop_younger_than_or_equal_to(
    prop: Union[str, None],
    days: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
):
    """
    Filter function which returns True if property younger than or equal to a relative amount of time since
    current time
    :param prop: prop value to check against - in UTC time
    :param days: (Optional) relative number of days since current time to compare against
    :param hours: (Optional) relative number of hours since current time to compare against
    :param minutes: (Optional) relative number of minutes since current time to compare against
    :param seconds: (Optional) relative number of seconds since current time to compare against

    By default, all time args are set to 0, i.e. now. Setting this to 10 seconds would mean 10 seconds in the past.
    You must give at least one non-zero argument (days, hours, minutes, seconds) otherwise a
    MissingMandatoryArgument exception will be thrown
    """
    if prop is None:
        return False
    prop_timestamp = datetime.strptime(prop, "%Y-%m-%dT%H:%M:%SZ").timestamp()
    given_timestamp = TimeUtils.get_timestamp_in_seconds(days, hours, minutes, seconds)
    return prop_timestamp >= given_timestamp


def prop_younger_than(
    prop: Union[str, None],
    days: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
):
    """
    Filter function which returns True if property younger than a relative amount of time since current time
    :param prop: prop value to check against - in UTC time
    :param days: (Optional) relative number of days since current time to compare against
    :param hours: (Optional) relative number of hours since current time to compare against
    :param minutes: (Optional) relative number of minutes since current time to compare against
    :param seconds: (Optional) relative number of seconds since current time to compare against

    By default, all time args are set to 0, i.e. now. Setting this to 10 seconds would mean 10 seconds in the past.
    You must give at least one non-zero argument (days, hours, minutes, seconds) otherwise a
    MissingMandatoryArgument exception will be thrown
    """
    if prop is None:
        return False
    prop_datetime = datetime.strptime(prop, "%Y-%m-%dT%H:%M:%SZ").timestamp()
    return prop_datetime > TimeUtils.get_timestamp_in_seconds(
        days, hours, minutes, seconds
    )


def prop_older_than_or_equal_to(
    prop: Union[str, None],
    days: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
):
    """
    Filter function which returns True if property older than or equal to a relative amount of time since current
    time
    :param prop: prop value to check against - in UTC time
    :param days: (Optional) relative number of days since current time to compare against
    :param hours: (Optional) relative number of hours since current time to compare against
    :param minutes: (Optional) relative number of minutes since current time to compare against
    :param seconds: (Optional) relative number of seconds since current time to compare against

    By default, all time args are set to 0, i.e. now. Setting this to 10 seconds would mean 10 seconds in the past.
    You must give at least one non-zero argument (days, hours, minutes, seconds) otherwise a
    MissingMandatoryArgument exception will be thrown
    """
    if prop is None:
        return False
    prop_datetime = datetime.strptime(prop, "%Y-%m-%dT%H:%M:%SZ").timestamp()
    return prop_datetime <= TimeUtils.get_timestamp_in_seconds(
        days, hours, minutes, seconds
    )


def prop_not_any_in(prop: Any, values: List[PropValue]) -> bool:
    """
    Filter function which returns true if a prop does not match any in a given list
    :param prop: prop value to check against
    :param values: a list of values to check against
    """
    if len(values) == 0:
        raise TypeError("values list must contain at least one item to match against")
    res = any(prop == val for val in values)
    return not res


def prop_any_in(prop: Any, values: List[PropValue]) -> bool:
    """
    Filter function which returns true if a prop matches any in a given list
    :param prop: prop value to check against
    :param values: a list of values to check against
    """
    if len(values) == 0:
        raise TypeError("values list must contain at least one item to match against")
    return any(prop == val for val in values)


def prop_not_equal_to(prop: Any, value: PropValue) -> bool:
    """
    Filter function which returns true if a prop is not equal to a given value
    :param prop: prop value to check against
    :param value: given value to check against
    """
    return not prop == value


def prop_equal_to(prop: Any, value: PropValue) -> bool:
    """
    Filter function which returns true if a prop is equal to a given value
    :param prop: prop value to check against
    :param value: given value to check against
    """
    return prop == value


def prop_less_than(prop: Union[int, float, None], value: Union[int, float]) -> bool:
    """
    Filter function which returns true if a prop is less than a given value
    :param prop: prop value to check against
    :param value: given value to check against
    """
    if prop is None:
        return False
    return prop < value


def prop_greater_than(prop: Union[int, float, None], value: Union[int, float]) -> bool:
    """
    Filter function which returns true if a prop is greater than a given value
    :param prop: prop value to check against
    :param value: given value to check against
    """
    if prop is None:
        return False
    return prop > value


def prop_less_than_or_equal_to(
    prop: Union[int, float, None], value: Union[int, float]
) -> bool:
    """
    Filter function which returns true if a prop is less than or equal to a given value
    :param prop: prop value to check against
    :param value: given value to check against
    """
    if prop is None:
        return False
    return prop <= value


def prop_greater_than_or_equal_to(
    prop: Union[int, float, None], value: Union[int, float]
) -> bool:
    """
    Filter function which returns true if a prop is greater than or equal to a given value
    :param prop: prop value to check against
    :param value: given value to check against
    """
    if prop is None:
        return False
    return prop >= value


def prop_matches_regex(prop: Union[str, None], value: str) -> bool:
    """
    Filter function which returns true if a prop matches a regex pattern
    :param prop: prop value to check against
    :param value: a string which can be converted into a valid regex pattern to run
    """
    if prop is None:
        return False
    res = re.match(re.compile(rf"{value}"), prop)
    return bool(res)


def prop_list_contains(prop: Union[List, None], values: Union[PropValue, List]) -> bool:
    """
    Filter function which returns true if a prop (a list) contains a value or sublist
    :param prop: prop list to check against
    :param values: a value or sublist of values to check if the prop list contains it
    :return:
    """
    if prop is None:
        return False

    if isinstance(values, list):
        return all(item in prop for item in values)
    return values in prop


def prop_list_not_contains(
    prop: Union[List, None], values: Union[PropValue, List]
) -> bool:
    """
    Filter function which returns true if a prop (a list) DOES NOT contain a given value or sublist
    :param prop: prop list to check against
    :param values: a value or sublist of values to check if the prop list contains it
    :return:
    """
    return not prop_list_contains(prop, values)
