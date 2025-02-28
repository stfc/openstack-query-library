from unittest.mock import MagicMock, NonCallableMock

import pytest

from openstackquery.handlers.client_side_handler import ClientSideHandler
from openstackquery.enums.query_presets import QueryPresets
from tests.mocks.mocked_props import MockProperties


@pytest.fixture(scope="function", name="filter_test_instance")
def instance_fixture():
    """
    Returns an instance with a mocked filter function mappings
    """

    # sets filter function mappings so that PROP_1 is valid for all client_side
    _filter_function_mappings = {
        preset: [MockProperties.PROP_1] for preset in QueryPresets
    }

    return ClientSideHandler(_filter_function_mappings)


@pytest.fixture(scope="function", name="run_client_filter_test")
def run_client_filter_test_fixture(filter_test_instance):
    """
    fixture to run a test cases for each client-side filter function
    """

    def _run_client_filter_test(preset, prop_value, mock_filter_func_kwargs):
        """
        runs a test case by calling get_filter_func for generic handler
        with a given preset, prop return value and value to compare against.
        :param preset: preset (mapped to filter func we want to test)
        :param prop_value: property value to test filter func with
        :param mock_filter_func_kwargs: extra arguments to setup/configure filter function

        """
        prop_func = MagicMock()
        prop_func.return_value = prop_value

        filter_func = filter_test_instance.get_filter_func(
            preset, MockProperties.PROP_1, prop_func, mock_filter_func_kwargs
        )

        mock_obj = NonCallableMock()
        res = filter_func(mock_obj)
        prop_func.assert_called_once_with(mock_obj)
        return res

    return _run_client_filter_test
