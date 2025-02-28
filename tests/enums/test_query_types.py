import pytest

from openstackquery.enums.query_types import QueryTypes
from openstackquery.exceptions.parse_query_error import ParseQueryError


@pytest.mark.parametrize(
    "expected_prop,test_values",
    [
        (QueryTypes.FLAVOR_QUERY, ["flavor_query", "flavor", "flavors", "flavorquery"]),
        (
            QueryTypes.PROJECT_QUERY,
            ["project_query", "project", "projects", "projectquery"],
        ),
        (
            QueryTypes.SERVER_QUERY,
            [
                "server_query",
                "vm",
                "vms",
                "vmquery",
                "server",
                "servers",
                "serverquery",
            ],
        ),
        (QueryTypes.USER_QUERY, ["user_query", "user", "users", "userquery"]),
        (QueryTypes.IMAGE_QUERY, ["image_query", "image", "images", "imagequery"]),
        (
            QueryTypes.HYPERVISOR_QUERY,
            ["hypervisor_query", "hypervisor", "hypervisors", "hypervisorquery"],
        ),
    ],
)
def test_query_presets_serialization(
    expected_prop, test_values, property_variant_generator
):
    """Test all query preset name formats can be correctly serialized."""
    for variant in property_variant_generator(test_values):
        assert QueryTypes.from_string(variant) is expected_prop


def test_get_preset_from_string_invalid():
    """
    Tests that get_preset_from_string returns error if given an invalid alias
    """
    with pytest.raises(ParseQueryError):
        QueryTypes.from_string("invalid-alias")
