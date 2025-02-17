from unittest.mock import MagicMock, NonCallableMock, patch
import pytest

from openstackquery.runners.server_runner import ServerRunner
from openstackquery.exceptions.parse_query_error import ParseQueryError


@pytest.fixture(name="instance")
def instance_fixture(mock_marker_prop_func):
    """
    Returns an instance to run tests with
    """
    return ServerRunner(marker_prop_func=mock_marker_prop_func)


def test_parse_meta_params_ambiguous(instance):
    """
    Tests parse_meta_params method when given both from_project and all_project arguments
    should raise an error
    """
    with pytest.raises(ParseQueryError):
        instance.parse_meta_params(
            NonCallableMock(),
            from_projects=["project_id1", "project_id2"],
            all_projects=True,
        )


def test_parse_meta_params_with_all_projects_no_admin(instance):
    """
    Tests parse_meta_params with no as_admin given
    method should raise error because all_projects won't work without admin being set
    """
    with pytest.raises(ParseQueryError):
        instance.parse_meta_params(NonCallableMock(), all_projects=True, as_admin=False)


def test_parse_meta_params_with_all_projects(instance):
    """
    Tests parse_meta_params with all_projects and as_admin set
    method should return meta params with only all_tenants set to true
    """
    mock_connection = MagicMock()
    res = instance.parse_meta_params(mock_connection, all_projects=True, as_admin=True)
    assert list(res.keys()) == ["all_tenants"]


@patch("openstackquery.runners.runner_utils.RunnerUtils.parse_projects")
def test_parse_meta_params_with_from_projects_as_admin(mock_parse_projects, instance):
    """
    Tests parse_meta_params with valid from_projects argument and as_admin = True
    method should call RunnerUtils.parse_projects to get project_ids and populate meta-param dictionary
    should also set all_tenants = True
    """
    mock_connection = MagicMock()
    mock_from_projects = NonCallableMock()
    res = instance.parse_meta_params(
        mock_connection, from_projects=mock_from_projects, as_admin=True
    )

    mock_parse_projects.assert_called_once_with(mock_connection, mock_from_projects)

    assert not set(res.keys()).difference({"projects", "all_tenants"})
    assert res["projects"] == mock_parse_projects.return_value
    assert res["all_tenants"] is True


@patch("openstackquery.runners.runner_utils.RunnerUtils.parse_projects")
def test_parse_meta_params_with_no_args(mock_parse_projects, instance):
    """
    Tests parse_meta_params with no args
    method should call RunnerUtils.parse_projects on current project_id and populate meta-param dictionary
    """

    mock_connection = MagicMock()
    res = instance.parse_meta_params(mock_connection)

    mock_parse_projects.assert_called_once_with(
        mock_connection, [mock_connection.current_project_id]
    )

    assert not set(res.keys()).difference({"projects"})
    assert res["projects"] == mock_parse_projects.return_value


def test_run_query_project_meta_arg_preset_duplication(instance):
    """
    Tests that an error is raised when run_query is called with filter kwargs which contains project_id and with
    meta_params that also contain projects - i.e there's a mismatch in which projects to search
    """
    with pytest.raises(ParseQueryError):
        instance.run_query(
            NonCallableMock(),
            filter_kwargs={"project_id": "proj1"},
            projects=["proj2", "proj3"],
        )


@patch("openstackquery.runners.runner_utils.RunnerUtils.run_paginated_query")
def test_run_query_with_meta_arg_projects_with_server_side_queries(
    mock_run_paginated_query, instance, mock_marker_prop_func
):
    """
    Tests run_query method when meta arg projects given method should for each project:
        - update filter kwargs to include "project_id": <id of project>
        - run _run_paginated_query with updated filter_kwargs
    """
    mock_run_paginated_query.side_effect = [
        ["server1", "server2"],
        ["server3", "server4"],
    ]
    mock_filter_kwargs = {"arg1": "val1"}

    projects = ["project-id1", "project-id2"]
    mock_connection = MagicMock()
    res = instance.run_query(
        mock_connection,
        filter_kwargs=mock_filter_kwargs,
        projects=projects,
    )

    for project in projects:
        mock_run_paginated_query.assert_any_call(
            mock_connection.compute.servers,
            mock_marker_prop_func,
            {"project_id": project, **mock_filter_kwargs},
        )

    assert res == ["server1", "server2", "server3", "server4"]


@patch("openstackquery.runners.runner_utils.RunnerUtils.run_paginated_query")
def test_run_query_meta_arg_all_tenants_no_projects(
    mock_run_paginated_query, instance, mock_marker_prop_func
):
    """
    Tests run_query method when meta arg all_tenants given
    """
    mock_run_paginated_query.return_value = ["server1", "server2"]
    mock_connection = MagicMock()

    res = instance.run_query(mock_connection, filter_kwargs={}, all_tenants=True)
    mock_run_paginated_query.assert_called_once_with(
        mock_connection.compute.servers,
        mock_marker_prop_func,
        {"all_tenants": True},
    )
    assert res == ["server1", "server2"]


@patch("openstackquery.runners.runner_utils.RunnerUtils.run_paginated_query")
def test_run_query_with_meta_arg_projects_with_no_server_queries(
    mock_run_paginated_query, instance, mock_marker_prop_func
):
    """
    Tests run_query method when meta arg projects given
    method should for each project run without any filter kwargs
    """
    mock_run_paginated_query.side_effect = [
        ["server1", "server2"],
        ["server3", "server4"],
    ]
    projects = ["project-id1", "project-id2"]
    mock_connection = MagicMock()

    res = instance.run_query(mock_connection, filter_kwargs={}, projects=projects)

    for project in projects:
        mock_run_paginated_query.assert_any_call(
            mock_connection.compute.servers,
            mock_marker_prop_func,
            {"project_id": project},
        )

    assert res == ["server1", "server2", "server3", "server4"]
