from unittest.mock import MagicMock, NonCallableMock, patch, call
import pytest

from openstackquery.structs.resource_provider_usage import ResourceProviderUsage
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


@patch("openstackquery.runners.runner_utils.RunnerUtils.run_paginated_query")
@patch("openstackquery.runners.hypervisor_runner.HypervisorRunner.get_hv_usage_data")
def test_run_query_no_server_filters(
    mock_get_hv_usage_data,
    mock_run_paginated_query,
    instance,
    mock_marker_prop_func,
):
    """
    Tests that run_query method works expectedly with no server-side filters
    """

    mock_hv1 = {"id": "1", "name": "hv1"}
    mock_hv1_rpusage = NonCallableMock()
    mock_hv2 = {"id": "2", "name": "hv2"}
    mock_hv2_rpusage = NonCallableMock()

    mock_get_hv_usage_data.return_value = {
        "hv1": mock_hv1_rpusage,
        "hv2": mock_hv2_rpusage,
    }

    mock_run_paginated_query.return_value = [mock_hv1, mock_hv2]

    mock_connection = MagicMock()

    res = instance.run_query(
        mock_connection,
        filter_kwargs=None,
    )

    mock_run_paginated_query.assert_called_once_with(
        mock_connection.compute.hypervisors,
        mock_marker_prop_func,
        {"details": True},
    )

    assert res[0].hv["name"] == "hv1"
    assert res[0].usage == mock_hv1_rpusage
    assert res[1].hv["name"] == "hv2"
    assert res[1].usage == mock_hv2_rpusage


@pytest.fixture(name="mock_inventory_responses")
def mock_inventory_responses_fixture():
    """
    func to replace conn.placement.resource_provider_inventories, returning known "total" values
    """

    def _mock_setup_inventory(results):
        def _mock_resource_provider_inventories(_, resource_class):
            return results.get(resource_class, None)

        return _mock_resource_provider_inventories

    return _mock_setup_inventory


@pytest.mark.parametrize(
    "test_case",
    [
        # test case for single provider with all inventory resources"
        {
            "providers": [{"id": "id1", "name": "foo"}],
            "usages": {"VCPU": 4, "MEMORY_MB": 8192, "DISK_GB": 100},
            "inventories": {
                "VCPU": [{"total": 16}],
                "MEMORY_MB": [{"total": 32768}],
                "DISK_GB": [{"total": 500}],
            },
            "expected_results": {
                "foo": ResourceProviderUsage(
                    vcpus_used=4,
                    memory_mb_used=8192,
                    disk_gb_used=100,
                    vcpus_avail=16,
                    memory_mb_avail=32768,
                    disk_gb_avail=500,
                    vcpus=20,
                    memory_mb_size=40960,
                    disk_gb_size=600,
                )
            },
        },
        # "test case for single provider with no inventory resources",
        {
            "providers": [{"id": "id1", "name": "foo"}],
            "usages": {"VCPU": 0, "MEMORY_MB": 0, "DISK_GB": 0},
            "inventories": {},
            "expected_results": {
                "foo": ResourceProviderUsage(
                    vcpus_used=0,
                    memory_mb_used=0,
                    disk_gb_used=0,
                    vcpus_avail=0,
                    memory_mb_avail=0,
                    disk_gb_avail=0,
                    vcpus=0,
                    memory_mb_size=0,
                    disk_gb_size=0,
                )
            },
        },
        # "test case for multiple providers with all inventory resources",
        {
            "name": "multiple_providers",
            "providers": [
                {"id": "id-0", "name": "provider-0"},
                {"id": "id-1", "name": "provider-1"},
                {"id": "id-2", "name": "provider-2"},
            ],
            "usages": {"VCPU": 4, "MEMORY_MB": 8192, "DISK_GB": 100},
            "inventories": {
                "VCPU": [{"total": 16}, {"total": 16}],
                "MEMORY_MB": [{"total": 500}, {"total": 1000}],
                "DISK_GB": [{"total": 500}, {"total": 1500}],
            },
            "expected_results": {
                f"provider-{i}": ResourceProviderUsage(
                    vcpus_used=4,
                    memory_mb_used=8192,
                    disk_gb_used=100,
                    vcpus_avail=32,
                    memory_mb_avail=1500,
                    disk_gb_avail=2000,
                    vcpus=36,
                    memory_mb_size=9692,
                    disk_gb_size=2100,
                )
                for i in range(3)
            },
        },
    ],
)
@patch("openstackquery.runners.hypervisor_runner.exceptions")
def test_get_hv_usage_data(
    mock_exceptions, instance, mock_inventory_responses, test_case
):
    """Unified test for get_hv_usage_data under different scenarios"""
    mock_connection = MagicMock()

    # Set up providers
    providers = test_case["providers"]
    mock_connection.placement.resource_providers.return_value = providers

    # Set up usage response
    mock_connection.session.get.return_value.json.return_value = {
        "usages": test_case["usages"]
    }

    # Set up inventory responses
    mock_connection.placement.resource_provider_inventories = MagicMock(
        wraps=mock_inventory_responses(test_case["inventories"])
    )

    # Execute
    results = instance.get_hv_usage_data(mock_connection)

    # Verify basic calls
    mock_connection.placement.resource_providers.assert_called_once_with()

    # Verify inventory calls for each provider
    for provider in providers:
        mock_connection.placement.resource_provider_inventories.assert_has_calls(
            [
                call(provider, resource_class="VCPU"),
                call(provider, resource_class="MEMORY_MB"),
                call(provider, resource_class="DISK_GB"),
            ]
        )

    # Verify usage API calls
    assert mock_exceptions.raise_from_response.call_count == len(providers)
    for provider in providers:
        mock_connection.session.get.assert_has_calls(
            [
                call(
                    f"resource_providers/{provider['id']}/usages",
                    endpoint_filter={"service_type": "placement"},
                )
            ]
        )

    # Verify results
    assert len(results) == len(test_case["expected_results"])

    for rp_name, rp_obj in test_case["expected_results"].items():
        assert results[rp_name] == rp_obj
