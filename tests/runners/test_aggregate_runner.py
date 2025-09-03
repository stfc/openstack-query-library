from unittest.mock import MagicMock, NonCallableMock

import pytest

from openstackquery.runners.aggregate_runner import AggregateRunner


@pytest.fixture(name="instance")
def instance_fixture(mock_marker_prop_func):
    """
    Returns an instance of AggregateRunner to run tests with
    """
    return AggregateRunner(marker_prop_func=mock_marker_prop_func)


def test_parse_query_params(instance):
    """
    Test that parse_meta_params returns an empty dict - AggregateRunner accepts no meta-params currently
    """
    assert (
        instance.parse_meta_params(
            NonCallableMock(), **{"arg1": "val1", "arg2": "val2"}
        )
        == {}
    )


def test_run_query_no_server_filters(instance):
    """
    Test that run_query returns correct results when no filter_kwargs are passed
    """
    mock_connection = MagicMock()
    mock_connection.compute.aggregates.return_value = [
        "aggregate1",
        "aggregate2",
        "aggregate3",
    ]

    result = instance.run_query(mock_connection, filter_kwargs=None)

    mock_connection.compute.aggregates.assert_called_once_with()
    assert result == mock_connection.compute.aggregates.return_value


def test_run_query_with_empty_filter_dict(instance):
    """
    Test that run_query returns correct results when empty filter_kwargs are passed
    """
    mock_connection = MagicMock()
    mock_connection.compute.aggregates.return_value = ["aggregateA"]

    result = instance.run_query(mock_connection, filter_kwargs={})

    mock_connection.compute.aggregates.assert_called_once_with()
    assert result == mock_connection.compute.aggregates.return_value
