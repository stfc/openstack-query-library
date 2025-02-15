from unittest.mock import MagicMock, NonCallableMock, patch, call
import pytest

from openstackquery.runners.placement_runner import PlacementRunner


@pytest.fixture(name="instance")
def instance_fixture(mock_marker_prop_func):
    """
    Returns an instance to run tests with
    """
    return PlacementRunner(marker_prop_func=mock_marker_prop_func)


@pytest.fixture
def mock_inventory_responses():
    """
    func to replace conn.placement.resource_provider_inventories, returning known "total" values
    """

    def _mock_setup_inventory(results):
        def _mock_resource_provider_inventories(_, resource_class):
            return results.get(resource_class, None)

        return _mock_resource_provider_inventories

    return _mock_setup_inventory


def test_parse_query_params(instance):
    """
    tests that parse_query_params returns empty dict - PlacementQuery accepts no meta-params currently
    """
    assert (
        instance.parse_meta_params(
            NonCallableMock(), **{"arg1": "val1", "arg2": "val2"}
        )
        == {}
    )


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
            "expected_results": [
                {
                    "id": "id1",
                    "name": "foo",
                    "vcpu_used": 4,
                    "memory_mb_used": 8192,
                    "disk_gb_used": 100,
                    "vcpu_avail": 16,
                    "memory_mb_avail": 32768,
                    "disk_gb_avail": 500,
                }
            ],
        },
        # "test case for single provider with no inventory resources",
        {
            "providers": [{"id": "id1", "name": "foo"}],
            "usages": {"VCPU": 0, "MEMORY_MB": 0, "DISK_GB": 0},
            "inventories": {},
            "expected_results": [
                {
                    "id": "id1",
                    "name": "foo",
                    "vcpu_used": 0,
                    "memory_mb_used": 0,
                    "disk_gb_used": 0,
                    "vcpu_avail": 0,
                    "memory_mb_avail": 0,
                    "disk_gb_avail": 0,
                }
            ],
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
            "expected_results": [
                {
                    "id": f"id-{i}",
                    "name": f"provider-{i}",
                    "vcpu_used": 4,
                    "memory_mb_used": 8192,
                    "disk_gb_used": 100,
                    "vcpu_avail": 32,
                    "memory_mb_avail": 1500,
                    "disk_gb_avail": 2000,
                }
                for i in range(3)
            ],
        },
    ],
)
@patch("openstackquery.runners.placement_runner.exceptions")
def test_run_query(mock_exceptions, instance, mock_inventory_responses, test_case):
    """Unified test for run_query under different scenarios"""
    mock_connection = MagicMock()

    # Set up providers
    providers = []
    for provider_data in test_case["providers"]:
        provider = MagicMock()
        provider.id = provider_data["id"]
        provider.name = provider_data["name"]
        providers.append(provider)
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
    results = instance.run_query(mock_connection, {"arg1": "foo", "arg2": "bar"})

    # Verify basic calls
    mock_connection.placement.resource_providers.assert_called_once_with(
        arg1="foo", arg2="bar"
    )

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
                    f"resource_providers/{provider.id}/usages",
                    endpoint_filter={"service_type": "placement"},
                )
            ]
        )

    # Verify results
    assert len(results) == len(test_case["expected_results"])
    for result, expected in zip(results, test_case["expected_results"]):
        assert result.id == expected["id"]
        assert result.name == expected["name"]
        assert result.vcpu_used == expected["vcpu_used"]
        assert result.memory_mb_used == expected["memory_mb_used"]
        assert result.disk_gb_used == expected["disk_gb_used"]
        assert result.vcpu_avail == expected["vcpu_avail"]
        assert result.memory_mb_avail == expected["memory_mb_avail"]
        assert result.disk_gb_avail == expected["disk_gb_avail"]


def test_run_query_empty_no_filter_kwargs(instance):
    """test that run_query accepts no filter kwargs and does
    nothing if resource_providers query returns nothing"""

    mock_connection = MagicMock()
    mock_connection.placement.resource_providers.return_value = []
    results = instance.run_query(mock_connection, {})
    assert results == []
