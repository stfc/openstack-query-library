from unittest.mock import MagicMock, NonCallableMock, patch
import pytest

from openstackquery.runners.user_runner import UserRunner


@pytest.fixture(name="instance")
def instance_fixture(mock_marker_prop_func):
    """
    Returns an instance to run tests with
    """
    return UserRunner(marker_prop_func=mock_marker_prop_func)


def test_parse_meta_params_with_from_domain(instance):
    """
    Tests parse_meta_params with valid from_domain argument
    method should get domain id from a UserDomain enum by calling get_user_domain
    """
    mock_domain_name = NonCallableMock()
    mock_domain_id = NonCallableMock()
    mock_connection = MagicMock()
    mock_connection.identity.find_domain.return_value = {"id": mock_domain_id}

    res = instance.parse_meta_params(mock_connection, from_domain=mock_domain_name)
    mock_connection.identity.find_domain.assert_called_once_with(mock_domain_name)
    assert res == {"domain_id": mock_domain_id}


def test_parse_meta_params_no_from_domain(instance):
    """
    Tests parse_meta_params with no from_domain argument
    should return id of domain name "default"
    """
    mock_domain_id = NonCallableMock()
    mock_connection = MagicMock()
    mock_connection.identity.find_domain.return_value = {"id": mock_domain_id}

    res = instance.parse_meta_params(mock_connection)
    mock_connection.identity.find_domain.assert_called_once_with("default")
    assert res == {"domain_id": mock_domain_id}


@patch("openstackquery.runners.runner_utils.RunnerUtils.run_paginated_query")
def test_run_query_with_server_side_filters(
    mock_run_paginated_query, instance, mock_marker_prop_func
):
    """
    Tests the run_query method works expectedly - when meta arg domain id given
    method should:
        - update filter kwargs to include "domain_id": <domain id given>
        - run _run_paginated_query with updated filter_kwargs
    """
    mock_connection = MagicMock()
    mock_user_list = mock_run_paginated_query.return_value = [
        "user1",
        "user2",
        "user2",
        "user3",
    ]
    mock_filter_kwargs = {"arg1": "val1", "arg2": "val2"}
    mock_domain_id = "domain-id1"

    res = instance.run_query(
        mock_connection,
        filter_kwargs=mock_filter_kwargs,
        domain_id=mock_domain_id,
    )

    mock_run_paginated_query.assert_called_once_with(
        mock_connection.identity.users,
        mock_marker_prop_func,
        {**{"domain_id": mock_domain_id}, **mock_filter_kwargs},
    )
    assert res == mock_user_list


@patch("openstackquery.runners.runner_utils.RunnerUtils.run_paginated_query")
def test_run_query_with_no_server_filters(
    mock_run_paginated_query, instance, mock_marker_prop_func
):
    """
    Tests the run_query method works expectedly with no server side filters
    """

    mock_user_list = mock_run_paginated_query.return_value = [
        "user1",
        "user2",
        "user3",
    ]
    mock_connection = MagicMock()
    mock_filter_kwargs = None
    mock_domain_id = "domain-id1"
    res = instance.run_query(
        mock_connection,
        filter_kwargs=mock_filter_kwargs,
        domain_id=mock_domain_id,
    )

    mock_run_paginated_query.assert_called_once_with(
        mock_connection.identity.users,
        mock_marker_prop_func,
        {"domain_id": mock_domain_id},
    )
    assert res == mock_user_list


def test_run_query_returns_list(instance):
    """
    Tests that run_query correctly returns a list of entries
    """
    return_value = NonCallableMock()
    mock_connection = MagicMock()
    mock_connection.identity.find_user.return_value = return_value

    returned = instance.run_query(mock_connection, filter_kwargs={"id": "1"})
    mock_connection.identity.find_user.assert_called_once_with("1", ignore_missing=True)
    assert [return_value] == returned
