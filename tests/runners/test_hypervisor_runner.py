from unittest.mock import MagicMock, NonCallableMock, patch
import pytest

from openstackquery.runners.hypervisor_runner import HypervisorRunner


@pytest.fixture(name="instance")
def instance_fixture(mock_marker_prop_func):
    """
    Returns an instance to run tests with
    """
    return HypervisorRunner(marker_prop_func=mock_marker_prop_func)


def test_parse_query_params(instance):
    """
    tests that parse_query_params returns empty dict - HypervisorQuery accepts no meta-params currently
    """
    assert (
        instance.parse_meta_params(
            NonCallableMock(), **{"arg1": "val1", "arg2": "val2"}
        )
        == {}
    )


@patch("openstackquery.runners.hypervisor_runner.json.loads")
@patch("openstackquery.runners.runner_utils.RunnerUtils.run_paginated_query")
def test_run_query_no_server_filters(
    mock_run_paginated_query,
    mock_json_loads,
    instance,
    mock_marker_prop_func,
):
    """
    Tests that run_query method works expectedly with no server-side filters
    """

    mock_hv1 = MagicMock()
    mock_hv2 = MagicMock()

    mock_hv1.return_value = {"id": "1"}
    mock_hv2.return_value = {"id": "2"}

    mock_hv_list = mock_run_paginated_query.return_value = [
        mock_hv1,
        mock_hv2,
    ]

    mock_connection = MagicMock()

    vcpu_resource_class = MagicMock()
    vcpu_resource_class.resource_class = "VCPU"
    vcpu_resource_class.total = 128
    memory_resource_class = MagicMock()
    memory_resource_class.resource_class = "MEMORY_MB"
    memory_resource_class.total = 515264
    disk_resource_class = MagicMock()
    disk_resource_class.resource_class = "DISK_GB"
    disk_resource_class.total = 3510

    mock_connection.placement.resource_provider_inventories.return_value = (
        vcpu_resource_class,
        memory_resource_class,
        disk_resource_class,
    )

    mock_json_loads.return_value = {
        "usages": {"VCPU": 4, "MEMORY_MB": 8192, "DISK_GB": 10}
    }

    res = instance.run_query(
        mock_connection,
        filter_kwargs=None,
    )

    mock_run_paginated_query.assert_called_once_with(
        mock_connection.compute.hypervisors,
        mock_marker_prop_func,
        {"details": True},
    )

    assert mock_json_loads.call_count == 2

    assert res == mock_hv_list

    assert mock_hv1.resources == {
        "VCPU": {"total": 128, "usage": 4, "free": 124},
        "MEMORY_MB": {"total": 515264, "usage": 8192, "free": 507072},
        "DISK_GB": {"total": 3510, "usage": 10, "free": 3500},
    }
    assert mock_hv2.resources == {
        "VCPU": {"total": 128, "usage": 4, "free": 124},
        "MEMORY_MB": {"total": 515264, "usage": 8192, "free": 507072},
        "DISK_GB": {"total": 3510, "usage": 10, "free": 3500},
    }
