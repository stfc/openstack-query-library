from typing import Dict

from enums.enum_with_aliases import EnumWithAliases

from mappings.flavor_mapping import FlavorMapping
from mappings.image_mapping import ImageMapping
from mappings.project_mapping import ProjectMapping
from mappings.server_mapping import ServerMapping
from mappings.user_mapping import UserMapping
from mappings.hypervisor_mapping import HypervisorMapping

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

    @staticmethod
    def _get_aliases() -> Dict:
        return {
            QueryTypes.FLAVOR_QUERY: [
                "flavor",
                "flavors",
            ],
            QueryTypes.PROJECT_QUERY: [
                "project",
                "projects",
            ],
            QueryTypes.SERVER_QUERY: [
                "server",
                "servers",
            ],
            QueryTypes.USER_QUERY: ["user", "users"],
            QueryTypes.IMAGE_QUERY: ["image", "images"],
            QueryTypes.HYPERVISOR_QUERY: ["hypervisor", "hypervisors"],
        }
