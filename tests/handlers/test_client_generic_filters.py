import pytest
from openstackquery.exceptions.query_preset_mapping_error import QueryPresetMappingError
from openstackquery.enums.query_presets import QueryPresets


@pytest.fixture(name="test_corpus")
def corpus_fixture():
    """
    Returns a set of arguments to test against
    """
    return [1, "foo", None, {"a": "b"}]


def test_prop_equal_to(run_client_filter_test, test_corpus):
    """
    Tests that method prop_equal_to functions expectedly
    """
    for i in test_corpus:
        assert run_client_filter_test(QueryPresets.EQUAL_TO, i, {"value": i})
        assert not run_client_filter_test(
            QueryPresets.EQUAL_TO, i, {"value": "not_equal"}
        )


def test_prop_not_equal_to(run_client_filter_test, test_corpus):
    """
    Tests that method not_prop_equal_to functions expectedly
    """
    for i in test_corpus:
        assert run_client_filter_test(
            QueryPresets.NOT_EQUAL_TO, i, {"value": "not_equal"}
        )
        assert not run_client_filter_test(QueryPresets.NOT_EQUAL_TO, i, {"value": i})


def test_prop_any_in(run_client_filter_test):
    """
    Tests that method prop_any_in functions expectedly
    """
    assert run_client_filter_test(
        QueryPresets.ANY_IN, "val3", {"values": ["val1", "val2", "val3"]}
    )
    assert not run_client_filter_test(
        QueryPresets.ANY_IN, "val4", {"values": ["val1", "val2", "val3"]}
    )


def test_prop_any_in_empty_list(run_client_filter_test):
    """
    Tests that method prop_any_in when given empty list raise error
    """
    with pytest.raises(QueryPresetMappingError):
        run_client_filter_test(QueryPresets.ANY_IN, "val3", {"values": []})


def test_prop_not_any_in(run_client_filter_test):
    """
    Tests that method prop_any_not_in functions expectedly
    """
    assert run_client_filter_test(
        QueryPresets.NOT_ANY_IN, "val4", {"values": ["val1", "val2", "val3"]}
    )
    assert not run_client_filter_test(
        QueryPresets.NOT_ANY_IN, "val3", {"values": ["val1", "val2", "val3"]}
    )


def test_prop_not_any_in_empty_list(run_client_filter_test):
    """
    Tests that method prop_any_not_in when given empty list raise error
    """
    with pytest.raises(QueryPresetMappingError):
        run_client_filter_test(QueryPresets.NOT_ANY_IN, "val3", {"values": []})
