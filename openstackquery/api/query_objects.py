from typing import TYPE_CHECKING, Type

from openstackquery.mappings.aggregate_mapping import AggregateMapping
from openstackquery.mappings.flavor_mapping import FlavorMapping
from openstackquery.mappings.hypervisor_mapping import HypervisorMapping
from openstackquery.mappings.image_mapping import ImageMapping
from openstackquery.mappings.mapping_interface import MappingInterface
from openstackquery.mappings.project_mapping import ProjectMapping
from openstackquery.mappings.server_mapping import ServerMapping
from openstackquery.mappings.user_mapping import UserMapping

if TYPE_CHECKING:
    from openstackquery.api.query_api import QueryAPI


def get_common(query_mapping: Type[MappingInterface]) -> "QueryAPI":
    """
    helper function to create query object from given mapping class
    using QueryFactory
    :param query_mapping: a mapping class that defines property, runner and handler mappings
    """
    # pylint: disable=import-outside-toplevel
    from openstackquery.api.query_api import QueryAPI
    from openstackquery.query_factory import QueryFactory

    return QueryAPI(QueryFactory.build_query_deps(query_mapping))


# disable this so that we can write functions that mimic a query object
# pylint:disable=invalid-name


def ServerQuery() -> "QueryAPI":
    """
    Simple helper function to setup a query using a factory
    """
    return get_common(ServerMapping)


def UserQuery() -> "QueryAPI":
    """
    Simple helper function to setup a query using a factory
    """
    return get_common(UserMapping)


def FlavorQuery() -> "QueryAPI":
    """
    Simple helper function to setup a query using a factory
    """
    return get_common(FlavorMapping)


def ProjectQuery() -> "QueryAPI":
    """
    Simple helper function to setup a query using a factory
    """
    return get_common(ProjectMapping)


def ImageQuery() -> "QueryAPI":
    """
    Simple helper function to setup a query using a factory
    """
    return get_common(ImageMapping)


def HypervisorQuery() -> "QueryAPI":
    """
    Simple helper function to setup a query using a factory
    """
    return get_common(HypervisorMapping)


def AggregateQuery() -> "QueryAPI":
    """
    Simple helper function to setup a query using a factory
    """
    return get_common(AggregateMapping)
