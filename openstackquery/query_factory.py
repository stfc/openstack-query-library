from typing import Type

from openstackquery.mappings.mapping_interface import MappingInterface
from openstackquery.query_blocks.query_builder import QueryBuilder
from openstackquery.query_blocks.query_chainer import QueryChainer
from openstackquery.query_blocks.query_output import QueryOutput
from openstackquery.query_blocks.query_parser import QueryParser
from openstackquery.query_blocks.query_executor import QueryExecutor
from openstackquery.structs.query_components import QueryComponents


# pylint:disable=too-few-public-methods
class QueryFactory:
    """
    This class is used to construct a query object using a factory pattern.
    Decouples the API from the implementation
    """

    @staticmethod
    def build_query_deps(mapping_cls: Type[MappingInterface]) -> QueryComponents:
        """
        Composes objects that make up the query - to allow dependency injection
        :param mapping_cls: A mapping class which is used to configure query objects
        and the enum they are grouped by
        """
        prop_mapping = mapping_cls.get_prop_mapping()

        output = QueryOutput(prop_mapping)
        parser = QueryParser(prop_mapping)
        builder = QueryBuilder(
            prop_enum_cls=prop_mapping,
            client_side_handlers=mapping_cls.get_client_side_handlers().to_list(),
            server_side_handler=mapping_cls.get_server_side_handler(),
        )
        executor = QueryExecutor(
            prop_enum_cls=prop_mapping, runner_cls=mapping_cls.get_runner_mapping()
        )

        chainer = QueryChainer(chain_mappings=mapping_cls.get_chain_mappings())

        return QueryComponents(output, parser, builder, executor, chainer)
