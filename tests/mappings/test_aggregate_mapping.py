from openstackquery.enums.props.aggregate_properties import AggregateProperties
from openstackquery.enums.query_presets import QueryPresets
from openstackquery.handlers.server_side_handler import ServerSideHandler
from openstackquery.mappings.aggregate_mapping import AggregateMapping
from openstackquery.runners.aggregate_runner import AggregateRunner


def test_get_runner_mapping():
    """
    Tests get runner mapping returns an AggregateRunner
    """
    assert AggregateMapping.get_runner_mapping() == AggregateRunner


def test_get_prop_mapping():
    """
    Tests get prop mapping returns AggregateProperties
    """
    assert AggregateMapping.get_prop_mapping() == AggregateProperties


def test_get_server_side_handler_returns_correct_type():
    """
    Tests get server side handler returns a ServerSideHandler
    """
    assert isinstance(AggregateMapping.get_server_side_handler(), ServerSideHandler)


def test_client_side_handlers(client_side_test_mappings):
    """
    Tests client side handler mappings are correct.
    """
    date_prop_list = [
        AggregateProperties.AGGREGATE_DELETED_AT,
        AggregateProperties.AGGREGATE_UPDATED_AT,
        AggregateProperties.AGGREGATE_CREATED_AT,
    ]

    string_prop_list = [
        AggregateProperties.AGGREGATE_HOSTTYPE,
        AggregateProperties.AGGREGATE_HOST_IPS,
        AggregateProperties.AGGREGATE_LOCAL_STORAGE_TYPE,
        AggregateProperties.AGGREGATE_METADATA,
    ]

    integer_prop_list = [
        AggregateProperties.AGGREGATE_GPUNUM,
    ]

    handler = AggregateMapping.get_client_side_handlers()
    mappings = {
        QueryPresets.EQUAL_TO: ["*"],
        QueryPresets.NOT_EQUAL_TO: ["*"],
        QueryPresets.ANY_IN: ["*"],
        QueryPresets.NOT_ANY_IN: ["*"],
        QueryPresets.MATCHES_REGEX: string_prop_list,
        QueryPresets.NOT_MATCHES_REGEX: string_prop_list,
        QueryPresets.YOUNGER_THAN: date_prop_list,
        QueryPresets.YOUNGER_THAN_OR_EQUAL_TO: date_prop_list,
        QueryPresets.OLDER_THAN: date_prop_list,
        QueryPresets.OLDER_THAN_OR_EQUAL_TO: date_prop_list,
        QueryPresets.LESS_THAN: integer_prop_list,
        QueryPresets.LESS_THAN_OR_EQUAL_TO: integer_prop_list,
        QueryPresets.GREATER_THAN: integer_prop_list,
        QueryPresets.GREATER_THAN_OR_EQUAL_TO: integer_prop_list,
    }
    client_side_test_mappings(handler, mappings)


def test_get_chain_mappings():
    """
    Tests get_chain_mapping outputs None since there are no mappings.
    """
    assert AggregateMapping.get_chain_mappings() is None
