from dataclasses import dataclass

from openstackquery.query_blocks.query_builder import QueryBuilder
from openstackquery.query_blocks.query_chainer import QueryChainer
from openstackquery.query_blocks.query_output import QueryOutput
from openstackquery.query_blocks.query_parser import QueryParser
from openstackquery.query_blocks.query_executor import QueryExecutor


@dataclass
class QueryComponents:
    """
    A dataclass to hold configured objects that together make up parts of the query
    :param output: holds a configured QueryOutput object which is used to output the results of the query
        - and handles the select(), to_string(), to_html(), etc commands
    :param parser: holds a configured QueryParser object which is used to handle sort_by/group_by commands
    :param builder: holds a configured QueryBuilder object which is used to handler where() commands
    :param executor: holds a configured QueryExecute object which is used to execute the query
        - handles the run() command
    :param chainer: holds a configured QueryChainer object which is used to store query chain mappings
    """

    output: QueryOutput
    parser: QueryParser
    builder: QueryBuilder
    executor: QueryExecutor
    chainer: QueryChainer
