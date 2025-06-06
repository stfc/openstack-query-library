from unittest.mock import MagicMock, NonCallableMock, call

import pytest

from openstackquery.exceptions.parse_query_error import ParseQueryError
from openstackquery.exceptions.query_preset_mapping_error import QueryPresetMappingError

from openstackquery.handlers.client_side_handler import ClientSideHandler

from tests.mocks.mocked_query_presets import MockQueryPresets
from tests.mocks.mocked_props import MockProperties


@pytest.fixture(name="mock_filter_fn")
def mock_filter_instance():
    """
    Returns a mocked filter function
    """
    return MagicMock()


@pytest.fixture(name="instance")
def instance_fixture(mock_filter_fn):
    """
    Returns a function that will setup a client_side_handler with mocks
    """
    client_side_handler = ClientSideHandler(
        {
            MockQueryPresets.ITEM_1: ["*"],
            MockQueryPresets.ITEM_2: [MockProperties.PROP_1, MockProperties.PROP_2],
            MockQueryPresets.ITEM_3: [MockProperties.PROP_3, MockProperties.PROP_4],
        }
    )
    # pylint:disable=protected-access
    # we need to mock _filter_functions mappings to test functions that use them
    # but the mappings themselves are hardcoded into the class and should not be accessible
    client_side_handler._filter_functions = {MockQueryPresets.ITEM_1: mock_filter_fn}
    return client_side_handler


def test_get_supported_props(instance):
    """
    Tests that get_supported_props method works expectedly
    returns the props mapped to a preset
    """
    assert instance.get_supported_props(MockQueryPresets.ITEM_1) == ["*"]
    assert instance.get_supported_props(MockQueryPresets.ITEM_2) == [
        MockProperties.PROP_1,
        MockProperties.PROP_2,
    ]


def test_check_supported_preset_unknown(instance):
    """
    Tests that check_supported method, when preset_known returns False, return False
    """
    mock_preset = MockQueryPresets.ITEM_4
    mock_prop = NonCallableMock()
    res = instance.check_supported(mock_preset, mock_prop)
    assert not res


def test_check_supported_prop_unknown(instance):
    """
    Tests that check_supported method, when prop not supported by preset, return False
    """
    mock_preset = MockQueryPresets.ITEM_4
    mock_prop = NonCallableMock()
    res = instance.check_supported(mock_preset, mock_prop)
    assert not res


def test_check_supported_for_preset_that_supports_all(instance):
    """
    Tests that check_supported method, for a preset with '*' - check that it supports all props,
    all props should return True
    """
    mock_preset = MockQueryPresets.ITEM_1
    assert all(instance.check_supported(mock_preset, i) for i in list(MockProperties))


def test_check_preset_and_prop_supported(instance):
    """
    Tests that check_supported method works expectedly
    returns False if either Preset is not supported or Preset-Prop does not have a mapping
    """
    assert instance.check_supported(MockQueryPresets.ITEM_2, MockProperties.PROP_1)
    assert instance.check_supported(MockQueryPresets.ITEM_2, MockProperties.PROP_2)
    assert instance.check_supported(MockQueryPresets.ITEM_3, MockProperties.PROP_3)
    assert instance.check_supported(MockQueryPresets.ITEM_3, MockProperties.PROP_4)


@pytest.fixture(name="get_filter_func_runner")
def get_filter_func_runner_fixture(instance):
    """fixture that runs get_filter_func with valid kwargs"""

    def _get_filter_func_runner(mock_prop_func, mock_filter_func_kwargs=None):
        """
        function that runs get_filter_func with valid kwargs
        :param mock_prop_func: a mocked prop func
        :param mock_filter_func_kwargs: a mocked set of filter kwargs
        """

        filter_func = instance.get_filter_func(
            MockQueryPresets.ITEM_1,
            MockProperties.PROP_1,
            mock_prop_func,
            mock_filter_func_kwargs,
        )

        # run the filter function - invokes _filter_func_wrapper
        mock_obj = NonCallableMock()
        res = filter_func(mock_obj)
        mock_prop_func.assert_called_once_with(mock_obj)
        return res

    return _get_filter_func_runner


def test_get_filter_func_valid_kwargs(get_filter_func_runner, mock_filter_fn):
    """
    Tests calling get_filter_func with valid kwargs.
    get_filter_func will get a simple stub method that will output whatever value that kwarg "out" holds
    """
    mock_prop_func = MagicMock()
    mock_kwargs = {"arg1": "val1", "arg2": "val2"}

    res = get_filter_func_runner(mock_prop_func, mock_kwargs)

    mock_filter_fn.assert_has_calls(
        [
            # first call from _check_filter_func
            call(None, **mock_kwargs),
            # second call from _filter_func_wrapper
            call(mock_prop_func.return_value, **mock_kwargs),
        ]
    )
    assert res == mock_filter_fn.return_value


def test_get_filter_func_valid_kwargs_no_params(get_filter_func_runner, mock_filter_fn):
    """
    Tests calling get_filter_func with valid kwargs - filter takes no extra params.
    get_filter_func will get a simple stub method that will output whatever value that kwarg "out" holds
    """
    mock_prop_func = MagicMock()
    mock_kwargs = None

    res = get_filter_func_runner(mock_prop_func, mock_kwargs)

    mock_filter_fn.assert_has_calls(
        [
            # first call from _check_filter_func
            call(None),
            # second call from _filter_func_wrapper
            call(mock_prop_func.return_value),
        ]
    )
    assert res == mock_filter_fn.return_value


def test_get_filter_func_prop_func_raises_error(get_filter_func_runner, mock_filter_fn):
    """
    Tests calling get_filter_func with prop func that raises AttributeError when invoked
    filter_func_wrapper should return False in this case
    """
    mock_prop_func = MagicMock()
    mock_prop_func.side_effect = AttributeError
    mock_kwargs = None

    res = get_filter_func_runner(mock_prop_func, mock_kwargs)

    mock_filter_fn.assert_has_calls(
        [
            # first call from _check_filter_func
            call(None),
            # second call doesn't happen since prop func fails
        ]
    )
    assert res is False


def test_get_filter_func_preset_invalid(instance):
    """
    Tests get_filter_func method with invalid preset
    should raise QueryPresetMappingError
    """
    mock_prop_func = MagicMock()
    mock_kwargs = {"arg1": "val1", "arg2": "val2"}

    # when preset is invalid
    with pytest.raises(QueryPresetMappingError):
        instance.get_filter_func(
            MockQueryPresets.ITEM_4,
            MockProperties.PROP_1,
            mock_prop_func,
            mock_kwargs,
        )


def test_get_filter_func_prop_invalid(instance):
    """
    Tests get_filter_func when prop is not valid.
    Should raise QueryPresetMappingError
    """

    # when the preset is valid, but property is invalid
    with pytest.raises(QueryPresetMappingError):
        mock_prop_func = MagicMock()
        mock_kwargs = {"arg1": "val1", "arg2": "val2"}
        instance.get_filter_func(
            MockQueryPresets.ITEM_2,
            MockProperties.PROP_3,
            mock_prop_func,
            mock_kwargs,
        )


@pytest.mark.parametrize("error_type", [ParseQueryError, TypeError, NameError])
def test_get_filter_func_filter_raises_error(error_type, instance, mock_filter_fn):
    """
    Tests get_filter_func method when filter function raises an error.
    Should raise QueryPresetMappingError
    """
    mock_prop_func = MagicMock()
    mock_kwargs = {"arg1": "val1", "arg2": "val2"}
    mock_filter_fn.side_effect = error_type

    with pytest.raises(QueryPresetMappingError):
        instance.get_filter_func(
            MockQueryPresets.ITEM_1,
            MockProperties.PROP_1,
            mock_prop_func,
            mock_kwargs,
        )

    mock_filter_fn.assert_called_once_with(None, **mock_kwargs)
