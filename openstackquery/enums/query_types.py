from typing import Dict

from openstackquery.enums.enum_with_aliases import EnumWithAliases
from openstackquery.mappings.aggregate_mapping import AggregateMapping
from openstackquery.mappings.flavor_mapping import FlavorMapping
from openstackquery.mappings.hypervisor_mapping import HypervisorMapping
from openstackquery.mappings.image_mapping import ImageMapping
from openstackquery.mappings.project_mapping import ProjectMapping
from openstackquery.mappings.server_mapping import ServerMapping
from openstackquery.mappings.user_mapping import UserMapping

# pylint: disable=too-few-public-methods


class QueryTypes(EnumWithAliases):
    """
    Enum class which holds enums for different query objects. Used when
    specifying queries to chain to
    """

    FLAVOR_QUERY = FlavorMapping
    PROJECT_QUERY = ProjectMapping
    SERVER_QUERY = ServerMapping
    USER_QUERY = UserMapping
    IMAGE_QUERY = ImageMapping
    HYPERVISOR_QUERY = HypervisorMapping
    AGGREGATE_QUERY = AggregateMapping

    @staticmethod
    def _get_aliases() -> Dict:
        return {
            QueryTypes.FLAVOR_QUERY: [
                "flavor",
                "flavors",
                "flavorquery",
            ],
            QueryTypes.PROJECT_QUERY: [
                "project",
                "projects",
                "projectquery",
            ],
            QueryTypes.SERVER_QUERY: [
                "vm",
                "vms",
                "vmquery",
                "server",
                "servers",
                "serverquery",
            ],
            QueryTypes.USER_QUERY: [
                "user",
                "users",
                "userquery",
            ],
            QueryTypes.IMAGE_QUERY: [
                "image",
                "images",
                "imagequery",
            ],
            QueryTypes.HYPERVISOR_QUERY: [
                "hypervisor",
                "hypervisors",
                "hypervisorquery",
            ],
            QueryTypes.AGGREGATE_QUERY: ["aggregate", "aggregates", "aggregatequery"],
        }
