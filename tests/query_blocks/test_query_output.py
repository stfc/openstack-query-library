import json
from unittest.mock import MagicMock, NonCallableMock, call, patch

import pytest

from openstackquery.enums.props.server_properties import ServerProperties
from openstackquery.exceptions.parse_query_error import ParseQueryError
from openstackquery.query_blocks.query_output import QueryOutput
from tests.mocks.mocked_props import MockProperties


@pytest.fixture(name="instance")
def instance_fixture():
    """
    Returns an instance with mocked prop_enum_cls inject
    """
    mock_prop_enum_cls = MockProperties
    return QueryOutput(prop_enum_cls=mock_prop_enum_cls)


def test_selected_props(instance):
    """
    Tests that property method to get selected props works expectedly
    method should return self._props as a list
    """

    val = {
        MockProperties.PROP_1,
        MockProperties.PROP_2,
        MockProperties.PROP_3,
    }
    instance.selected_props = val
    assert instance.selected_props == list(val)


def test_selected_props_empty(instance):
    """
    Tests selected property method returns empty list when no props selected
    """
    assert instance.selected_props == []


def test_to_objects(instance):
    """
    Tests to_objects method with list results and no groups keyword given.
    Should call results_container.to_objects() and return as is
    """
    mock_results_container = MagicMock()
    mock_results_container.to_objects.return_value = NonCallableMock()
    res = instance.to_objects(mock_results_container)

    mock_results_container.to_objects.assert_called_once_with()
    assert res == mock_results_container.to_objects.return_value


def test_to_objects_ungrouped_results_with_group(instance):
    """
    Tests to_objects method with list results and groups keyword given.
    Should raise error
    """
    mock_results_container = MagicMock()
    mock_results_container.to_objects.return_value = [NonCallableMock()]
    with pytest.raises(ParseQueryError):
        instance.to_objects(mock_results_container, groups=["invalid-group"])


def test_to_objects_with_group_invalid(instance):
    """
    Tests to_objects method with dict results and groups keyword given.
    But groups provided contains invalid keys. Should raise error
    """
    mock_results_container = MagicMock()
    mock_results_container.to_objects.return_value = {"group1": [NonCallableMock()]}
    with pytest.raises(ParseQueryError):
        instance.to_objects(mock_results_container, groups=["invalid-group"])


def test_to_objects_with_group_valid(instance):
    """
    Tests to_objects method with dict results and groups keyword given.
    groups provided are valid keys. Should only return those keys
    """
    mock_results_container = MagicMock()
    groups = ["group1", "group2"]
    results_returned = {
        "group1": [NonCallableMock()],
        "group2": [NonCallableMock()],
        "group3": [NonCallableMock()],
    }
    expected = {k: results_returned[k] for k in groups}
    mock_results_container.to_objects.return_value = results_returned
    res = instance.to_objects(mock_results_container, groups=["group1", "group2"])
    mock_results_container.to_objects.assert_called_once_with()
    assert res == expected


def test_to_props(instance):
    """
    Tests to_props method with no extra params
    """
    mock_results_container = MagicMock()
    mock_results_container.to_props.return_value = NonCallableMock()
    res = instance.to_props(mock_results_container)
    mock_results_container.to_props.assert_called_once_with(*instance.selected_props)
    assert res == mock_results_container.to_props.return_value


def test_to_props_ungrouped_results_with_flatten(instance):
    """
    Tests to_props method with list results and flatten given.
    Should run flatten
    """
    mock_results_container = MagicMock()
    mock_results_container.to_props.return_value = [
        {"prop1": "val1", "prop2": "val2"},
        {"prop1": "val3", "prop2": "val4"},
        {"prop1": "val5", "prop2": "val6"},
    ]
    res = instance.to_props(mock_results_container, flatten=True)
    assert res == {"prop1": ["val1", "val3", "val5"], "prop2": ["val2", "val4", "val6"]}


def test_to_props_grouped_results_with_flatten(instance):
    """
    Tests to_props method with dict results and flatten given.
    Should run flatten on each group
    """
    mock_results_container = MagicMock()
    mock_results_container.to_props.return_value = {
        "group1": [
            {"prop1": "val1", "prop2": "val2"},
            {"prop1": "val3", "prop2": "val4"},
        ],
        "group2": [
            {"prop1": "val5", "prop2": "val6"},
            {"prop1": "val7", "prop2": "val8"},
        ],
    }

    res = instance.to_props(mock_results_container, flatten=True)
    assert res == {
        "group1": {"prop1": ["val1", "val3"], "prop2": ["val2", "val4"]},
        "group2": {"prop1": ["val5", "val7"], "prop2": ["val6", "val8"]},
    }


def test_to_props_results_empty_with_flatten(instance):
    """
    Tests to props method with empty list as results and flatten given
    should return None
    """
    mock_results_container = MagicMock()
    mock_results_container.to_props.return_value = []
    res = instance.to_props(mock_results_container, flatten=True)
    assert res is None


def test_to_props_grouped_results_with_flatten_and_group(instance):
    """
    Tests to_props method with dict results, with flatten and groups given.
    Should run flatten on each group
    """
    mock_results_container = MagicMock()
    mock_results_container.to_props.return_value = {
        "group1": [
            {"prop1": "val1", "prop2": "val2"},
            {"prop1": "val3", "prop2": "val4"},
        ],
        "group2": [
            {"prop1": "val5", "prop2": "val6"},
            {"prop1": "val7", "prop2": "val8"},
        ],
    }

    res = instance.to_props(mock_results_container, groups=["group1"], flatten=True)
    assert res == {"group1": {"prop1": ["val1", "val3"], "prop2": ["val2", "val4"]}}


@patch("openstackquery.query_blocks.query_output.tabulate")
def test_to_html_results_empty(mock_tabulate, instance):
    """
    Tests to_html method with no extra params and empty results
    """
    mock_results_container = MagicMock()
    mock_results_container.to_props.return_value = []
    mock_tabulate.return_value = "tabulate-output"
    res = instance.to_html(mock_results_container)

    mock_results_container.to_props.assert_called_once_with(*instance.selected_props)
    mock_tabulate.assert_not_called()
    assert res == "No results found<br/><br/>"


@patch("openstackquery.query_blocks.query_output.tabulate")
def test_to_html_ungrouped_results(mock_tabulate, instance):
    """
    Tests to_html method with no extra params and ungrouped results
    """
    mock_results_container = MagicMock()
    mock_results_container.to_props.return_value = [
        {"prop1": "val1", "prop2": "val2"},
        {"prop1": "val3", "prop2": "val4"},
    ]
    mock_tabulate.return_value = "tabulate-output"
    res = instance.to_html(mock_results_container)

    mock_results_container.to_props.assert_called_once_with(*instance.selected_props)
    mock_tabulate.assert_called_once_with(
        [["val1", "val2"], ["val3", "val4"]], ["prop1", "prop2"], tablefmt="html"
    )

    assert res == "tabulate-output<br/><br/>"


@patch("openstackquery.query_blocks.query_output.tabulate")
def test_to_html_grouped_results(mock_tabulate, instance):
    """
    Tests to_html method with no extra params and grouped results
    """
    mock_results_container = MagicMock()
    mock_results_container.to_props.return_value = {
        "group1": [
            {"prop1": "val1", "prop2": "val2"},
            {"prop1": "val3", "prop2": "val4"},
        ],
        "group2": [{"prop1": "val4", "prop2": "val5"}],
    }

    mock_tabulate.side_effect = ["tabulate-output-group1", "tabulate-output-group2"]

    res = instance.to_html(mock_results_container)

    mock_results_container.to_props.assert_called_once_with(*instance.selected_props)
    mock_tabulate.assert_has_calls(
        [
            call(
                [["val1", "val2"], ["val3", "val4"]],
                ["prop1", "prop2"],
                tablefmt="html",
            ),
            call([["val4", "val5"]], ["prop1", "prop2"], tablefmt="html"),
        ]
    )

    assert res == (
        "<b>group1:</b><br/>tabulate-output-group1<br/><br/>"
        "<b>group2:</b><br/>tabulate-output-group2<br/><br/>"
    )


@patch("openstackquery.query_blocks.query_output.tabulate")
def test_to_html_with_title(mock_tabulate, instance):
    """
    Tests to_html method with title param and ungrouped results
    """
    mock_results_container = MagicMock()
    mock_results_container.to_props.return_value = [
        {"prop1": "val1", "prop2": "val2"},
        {"prop1": "val3", "prop2": "val4"},
    ]
    mock_tabulate.return_value = "tabulate-output"
    res = instance.to_html(mock_results_container, title="mock-title")

    mock_results_container.to_props.assert_called_once_with(*instance.selected_props)
    mock_tabulate.assert_called_once_with(
        [["val1", "val2"], ["val3", "val4"]], ["prop1", "prop2"], tablefmt="html"
    )

    assert res == ("<b>mock-title:</b><br/>" "tabulate-output<br/><br/>")


@patch("openstackquery.query_blocks.query_output.tabulate")
def test_to_html_with_title_grouped_results(mock_tabulate, instance):
    """
    Tests to_html method with title param and grouped results
    """
    mock_results_container = MagicMock()
    mock_results_container.to_props.return_value = {
        "group1": [
            {"prop1": "val1", "prop2": "val2"},
            {"prop1": "val3", "prop2": "val4"},
        ],
        "group2": [{"prop1": "val4", "prop2": "val5"}],
    }

    mock_tabulate.side_effect = ["tabulate-output-group1", "tabulate-output-group2"]

    res = instance.to_html(mock_results_container, title="mock-title")

    mock_results_container.to_props.assert_called_once_with(*instance.selected_props)
    mock_tabulate.assert_has_calls(
        [
            call(
                [["val1", "val2"], ["val3", "val4"]],
                ["prop1", "prop2"],
                tablefmt="html",
            ),
            call([["val4", "val5"]], ["prop1", "prop2"], tablefmt="html"),
        ]
    )

    assert res == (
        "<b>mock-title:</b><br/>"
        "<b>group1:</b><br/>tabulate-output-group1<br/><br/>"
        "<b>group2:</b><br/>tabulate-output-group2<br/><br/>"
    )


@patch("openstackquery.query_blocks.query_output.tabulate")
def test_to_html_with_title_and_group(mock_tabulate, instance):
    """
    Tests to_html method with title and group params and grouped results
    """
    mock_results_container = MagicMock()
    mock_results_container.to_props.return_value = {
        "group1": [
            {"prop1": "val1", "prop2": "val2"},
            {"prop1": "val3", "prop2": "val4"},
        ],
        "group2": [{"prop1": "val4", "prop2": "val5"}],
    }

    mock_tabulate.side_effect = ["tabulate-output-group2"]

    res = instance.to_html(
        mock_results_container, title="mock-title", groups=["group2"]
    )

    mock_results_container.to_props.assert_called_once_with(*instance.selected_props)
    mock_tabulate.assert_called_once_with(
        [["val4", "val5"]], ["prop1", "prop2"], tablefmt="html"
    )

    assert res == (
        "<b>mock-title:</b><br/>" "<b>group2:</b><br/>tabulate-output-group2<br/><br/>"
    )


@patch("openstackquery.query_blocks.query_output.tabulate")
def test_to_string_results_empty(mock_tabulate, instance):
    """
    Tests to_string method with no extra params and empty results
    """
    mock_results_container = MagicMock()
    mock_results_container.to_props.return_value = []
    mock_tabulate.return_value = "tabulate-output"
    res = instance.to_string(mock_results_container)

    mock_results_container.to_props.assert_called_once_with(*instance.selected_props)
    mock_tabulate.assert_not_called()
    assert res == "No results found\n\n"


@patch("openstackquery.query_blocks.query_output.tabulate")
def test_to_string_ungrouped_results(mock_tabulate, instance):
    """
    Tests to_string method with no extra params and ungrouped results
    """
    mock_results_container = MagicMock()
    mock_results_container.to_props.return_value = [
        {"prop1": "val1", "prop2": "val2"},
        {"prop1": "val3", "prop2": "val4"},
    ]
    mock_tabulate.return_value = "tabulate-output"
    res = instance.to_string(mock_results_container)

    mock_results_container.to_props.assert_called_once_with(*instance.selected_props)
    mock_tabulate.assert_called_once_with(
        [["val1", "val2"], ["val3", "val4"]], ["prop1", "prop2"], tablefmt="grid"
    )

    assert res == "tabulate-output\n\n"


@patch("openstackquery.query_blocks.query_output.tabulate")
def test_to_string_grouped_results(mock_tabulate, instance):
    """
    Tests to_string method with no extra params and grouped results
    """
    mock_results_container = MagicMock()
    mock_results_container.to_props.return_value = {
        "group1": [
            {"prop1": "val1", "prop2": "val2"},
            {"prop1": "val3", "prop2": "val4"},
        ],
        "group2": [{"prop1": "val4", "prop2": "val5"}],
    }

    mock_tabulate.side_effect = ["tabulate-output-group1", "tabulate-output-group2"]

    res = instance.to_string(mock_results_container)

    mock_results_container.to_props.assert_called_once_with(*instance.selected_props)
    mock_tabulate.assert_has_calls(
        [
            call(
                [["val1", "val2"], ["val3", "val4"]],
                ["prop1", "prop2"],
                tablefmt="grid",
            ),
            call([["val4", "val5"]], ["prop1", "prop2"], tablefmt="grid"),
        ]
    )

    assert res == (
        "group1:\ntabulate-output-group1\n\n" "group2:\ntabulate-output-group2\n\n"
    )


@patch("openstackquery.query_blocks.query_output.tabulate")
def test_to_string_with_title(mock_tabulate, instance):
    """
    Tests to_string method with title param and ungrouped results
    """
    mock_results_container = MagicMock()
    mock_results_container.to_props.return_value = [
        {"prop1": "val1", "prop2": "val2"},
        {"prop1": "val3", "prop2": "val4"},
    ]
    mock_tabulate.return_value = "tabulate-output"
    res = instance.to_string(mock_results_container, title="mock-title")

    mock_results_container.to_props.assert_called_once_with(*instance.selected_props)
    mock_tabulate.assert_called_once_with(
        [["val1", "val2"], ["val3", "val4"]], ["prop1", "prop2"], tablefmt="grid"
    )

    assert res == ("mock-title:\n" "tabulate-output\n\n")


@patch("openstackquery.query_blocks.query_output.tabulate")
def test_to_string_with_title_grouped_results(mock_tabulate, instance):
    """
    Tests to_string method with title param and grouped results
    """
    mock_results_container = MagicMock()
    mock_results_container.to_props.return_value = {
        "group1": [
            {"prop1": "val1", "prop2": "val2"},
            {"prop1": "val3", "prop2": "val4"},
        ],
        "group2": [{"prop1": "val4", "prop2": "val5"}],
    }

    mock_tabulate.side_effect = ["tabulate-output-group1", "tabulate-output-group2"]

    res = instance.to_string(mock_results_container, title="mock-title")

    mock_results_container.to_props.assert_called_once_with(*instance.selected_props)
    mock_tabulate.assert_has_calls(
        [
            call(
                [["val1", "val2"], ["val3", "val4"]],
                ["prop1", "prop2"],
                tablefmt="grid",
            ),
            call([["val4", "val5"]], ["prop1", "prop2"], tablefmt="grid"),
        ]
    )

    assert res == (
        "mock-title:\n"
        "group1:\ntabulate-output-group1\n\n"
        "group2:\ntabulate-output-group2\n\n"
    )


@patch("openstackquery.query_blocks.query_output.tabulate")
def test_to_string_with_title_and_group(mock_tabulate, instance):
    """
    Tests to_string method with title and group params and grouped results
    """
    mock_results_container = MagicMock()
    mock_results_container.to_props.return_value = {
        "group1": [
            {"prop1": "val1", "prop2": "val2"},
            {"prop1": "val3", "prop2": "val4"},
        ],
        "group2": [{"prop1": "val4", "prop2": "val5"}],
    }

    mock_tabulate.side_effect = ["tabulate-output-group2"]

    res = instance.to_string(
        mock_results_container, title="mock-title", groups=["group2"]
    )

    mock_results_container.to_props.assert_called_once_with(*instance.selected_props)
    mock_tabulate.assert_called_once_with(
        [["val4", "val5"]], ["prop1", "prop2"], tablefmt="grid"
    )

    assert res == ("mock-title:\n" "group2:\ntabulate-output-group2\n\n")


def test_parse_select_with_select_all(instance):
    """
    tests that parse select works expectedly - when called from select_all() - no props given
    method should set props internal attribute to all available props supported by prop_handler
    """
    # if select_all flag set, get all props
    instance.parse_select(select_all=True)
    assert instance.selected_props == list(set(MockProperties))


def test_parse_select_given_args(instance):
    """
    tests that parse select works expectedly - when called from select() - where props args given
    method should set check each given prop to see if mapping exists in prop_handler and
    add to internal attribute set props
    """
    # if given props
    instance.parse_select(MockProperties.PROP_1, MockProperties.PROP_2)
    assert instance.selected_props, [MockProperties.PROP_1, MockProperties.PROP_2]


def test_parse_select_given_invalid(instance):
    """
    Tests that parse_select works expectedly
    method should raise error when given an invalid prop enum
    """

    # server prop enums are invalid here and should be picked up
    with pytest.raises(ParseQueryError):
        instance.parse_select(MockProperties.PROP_1, ServerProperties.SERVER_ID)


def test_parse_select_overwrites_old(instance):
    """
    Tests that parse_select overwrites old selected_props
    method should overwrite internal attribute selected_props if already set
    """
    instance.selected_props = [MockProperties.PROP_1]
    instance.parse_select(MockProperties.PROP_2)
    assert instance.selected_props == [MockProperties.PROP_2]


# pylint:disable=W0212 # Allow protected-access for tests


def test_convert_csv_to_string(instance):
    data = [
        {"a": 1, "b": 2},
        {"a": 3, "b": 4},
    ]
    csv_str = instance._convert_to_csv_string(data)
    expected_csv = "a,b\r\n1,2\r\n3,4"
    assert csv_str == expected_csv


def test_convert_to_csv_string_raises_on_empty_data(instance):
    with pytest.raises(RuntimeError):
        instance._convert_to_csv_string([])


def test_convert_to_csv_string_raises_on_empty_dict_keys(instance):
    with pytest.raises(RuntimeError):
        instance._convert_to_csv_string([{}])


def test_to_csv_ungrouped(instance):
    mock_results_container = MagicMock()
    mock_results_container.to_props.return_value = [
        {"prop1": "val1", "prop2": "val2"},
        {"prop1": "val3", "prop2": "val4"},
    ]
    # no groups, no flatten
    csv_output = instance.to_csv(mock_results_container)
    assert "prop1,prop2" in csv_output
    assert "val1,val2" in csv_output
    mock_results_container.to_props.assert_called_once_with(*instance.selected_props)


def test_to_csv_grouped(instance):
    mock_results_container = MagicMock()
    mock_results_container.to_props.return_value = {
        "group1": [
            {"prop1": "val1", "prop2": "val2"},
            {"prop1": "val3", "prop2": "val4"},
        ],
        "group2": [
            {"prop1": "val5", "prop2": "val6"},
        ],
    }
    csv_output = instance.to_csv(mock_results_container)
    # Expect group headers
    assert "# Group: group1" in csv_output
    assert "# Group: group2" in csv_output
    assert "prop1,prop2" in csv_output
    assert "val1,val2" in csv_output
    assert "val5,val6" in csv_output


def test_to_csv_grouped_with_flatten(instance):
    mock_results_container = MagicMock()
    mock_results_container.to_props.return_value = {
        "group1": [
            {"prop1": "val1", "prop2": "val2"},
            {"prop1": "val3", "prop2": "val4"},
        ],
        "group2": [
            {"prop1": "val5", "prop2": "val6"},
        ],
    }

    csv_output = instance.to_csv(mock_results_container, flatten_groups=True)

    # Expect a flat CSV with a "group" column added
    assert "group,prop1,prop2" in csv_output or "prop1,prop2,group" in csv_output
    assert "group1" in csv_output
    assert "group2" in csv_output
    assert "val1,val2" in csv_output
    assert "val5,val6" in csv_output
    # Should not contain group headers (as we are flattening)
    assert "# Group:" not in csv_output


def test_to_csv_with_group_filtering(instance):
    mock_results_container = MagicMock()
    # Simulate grouped results from the container
    grouped_data = {
        "group1": [
            {"prop1": "val1", "prop2": "val2"},
        ],
        "group2": [
            {"prop1": "val3", "prop2": "val4"},
        ],
    }
    mock_results_container.to_props.return_value = grouped_data

    # Patch the instance's _validate_groups method to simulate filtering
    filtered_data = {"group2": grouped_data["group2"]}
    instance._validate_groups = MagicMock(return_value=filtered_data)

    csv_output = instance.to_csv(mock_results_container, groups=["group2"])

    # Check that only group2 is present in the output
    assert "# Group: group2" in csv_output
    assert "val3,val4" in csv_output
    assert "# Group: group1" not in csv_output
    assert "val1,val2" not in csv_output

    instance._validate_groups.assert_called_once_with(grouped_data, ["group2"])


# pylint:enable=W0212


def test_to_json_empty_results(instance):
    """
    Tests to_json with no groups or flatten
    """
    mock_results_container = MagicMock()
    mock_results_container.to_props.return_value = []

    result = instance.to_json(mock_results_container)
    mock_results_container.to_props.assert_called_once_with(*instance.selected_props)

    assert json.loads(result) == []


def test_to_json_ungrouped_results(instance):
    mock_results_container = MagicMock()
    mock_results_container.to_props.return_value = [
        {"prop1": "val1", "prop2": "val2"},
        {"prop1": "val3", "prop2": "val4"},
    ]

    result = instance.to_json(mock_results_container)
    mock_results_container.to_props.assert_called_once_with(*instance.selected_props)
    parsed = json.loads(result)

    assert isinstance(parsed, list)

    assert parsed == mock_results_container.to_props.return_value


def test_to_json_grouped_results(instance):
    mock_results_container = MagicMock()
    grouped_data = {
        "group1": [
            {"prop1": "val1", "prop2": "val2"},
            {"prop1": "val3", "prop2": "val4"},
        ],
        "group2": [{"prop1": "val5", "prop2": "val6"}],
    }
    mock_results_container.to_props.return_value = grouped_data
    result = instance.to_json(mock_results_container)
    parsed = json.loads(result)
    assert isinstance(parsed, dict)
    assert set(parsed.keys()) == set(grouped_data.keys())
    assert parsed["group1"] == grouped_data["group1"]


def test_to_json_flatten_groups(instance):
    mock_results_container = MagicMock()
    grouped_data = {
        "group1": [{"prop1": "val1"}],
        "group2": [{"prop1": "val2"}],
    }
    mock_results_container.to_props.return_value = grouped_data
    # flatten_groups=True should merge groups with group info
    result = instance.to_json(mock_results_container, flatten_groups=True)
    parsed = json.loads(result)
    assert isinstance(parsed, list)
    assert any("group" in item for item in parsed)
    groups = {item["group"] for item in parsed}
    assert groups == {"group1", "group2"}


def test_to_json_pretty(instance):
    mock_results_container = MagicMock()
    data = [{"prop1": "val1"}]
    mock_results_container.to_props.return_value = data
    result = instance.to_json(mock_results_container, pretty=True)
    # Pretty JSON has newlines and indents
    assert result.startswith("[\n")
    parsed = json.loads(result)
    assert parsed == data


def test_to_json_with_groups_filter(instance):
    mock_results_container = MagicMock()
    grouped_data = {
        "group1": [{"prop1": "val1"}],
        "group2": [{"prop1": "val2"}],
    }
    mock_results_container.to_props.return_value = grouped_data
    # filtering only "group2"
    result = instance.to_json(mock_results_container, groups=["group2"])
    parsed = json.loads(result)
    assert set(parsed.keys()) == {"group2"}
