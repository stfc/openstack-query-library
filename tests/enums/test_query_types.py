import pytest

from openstackquery.enums.query_types import QueryTypes
from openstackquery.exceptions.parse_query_error import ParseQueryError


@pytest.mark.parametrize(
    "query_type",
    [
        "Flavor_Query",
        "FlAvOr_Query",
        "flavor_query",
        "flavor",
        "flavors",
        "flavorquery",
    ],
)
def test_flavor_query_serialization(query_type):
    """
    Tests that variants of FLAVOR_QUERY can be serialized
    """
    assert QueryTypes.from_string(query_type) is QueryTypes.FLAVOR_QUERY


@pytest.mark.parametrize(
    "query_type",
    [
        "Server_Query",
        "SeRvEr_QuErY",
        "server_query",
        "server",
        "servers",
        "serverquery",
    ],
)
def test_server_query_serialization(query_type):
    """
    Tests that variants of SERVER_QUERY can be serialized
    """
    assert QueryTypes.from_string(query_type) is QueryTypes.SERVER_QUERY


@pytest.mark.parametrize(
    "query_type",
    [
        "Project_Query",
        "PrOjEcT_Query",
        "project_query",
        "project",
        "projects",
        "projectquery",
    ],
)
def test_project_query_serialization(query_type):
    """
    Tests that variants of PROJECT_QUERY can be serialized
    """
    assert QueryTypes.from_string(query_type) is QueryTypes.PROJECT_QUERY


@pytest.mark.parametrize(
    "query_type",
    ["User_Query", "UsEr_QuEry", "user_query", "user", "users", "userquery"],
)
def test_user_query_serialization(query_type):
    """
    Tests that variants of USER_QUERY can be serialized
    """
    assert QueryTypes.from_string(query_type) is QueryTypes.USER_QUERY


@pytest.mark.parametrize(
    "query_type",
    ["Image_Query", "ImAgE_QuEry", "image_query", "image", "images", "imagequery"],
)
def test_image_query_serialization(query_type):
    """
    Tests that variants of IMAGE_QUERY can be serialized
    """
    assert QueryTypes.from_string(query_type) is QueryTypes.IMAGE_QUERY


@pytest.mark.parametrize(
    "query_type",
    [
        "Hypervisor_Query",
        "HyPeRvIsOr_QuErY",
        "hypervisor_query",
        "hypervisor",
        "hypervisors",
        "hypervisorquery",
    ],
)
def test_hypervisor_query_serialization(query_type):
    """
    Tests that variants of HYPERVISOR_QUERY can be serialized
    """
    assert QueryTypes.from_string(query_type) is QueryTypes.HYPERVISOR_QUERY


def test_invalid_serialization():
    """
    Tests that error is raised when passes invalid string
    """
    with pytest.raises(ParseQueryError):
        QueryTypes.from_string("some-invalid-string")
