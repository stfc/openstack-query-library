from typing import Type

from aliases import QueryChainMappings
from openstackquery.enums.props.image_properties import ImageProperties
from openstackquery.enums.props.server_properties import ServerProperties
from openstackquery.enums.query_presets import QueryPresets

from openstackquery.handlers.client_side_handler import ClientSideHandler
from openstackquery.handlers.server_side_handler import ServerSideHandler

from openstackquery.mappings.mapping_interface import MappingInterface
from openstackquery.runners.image_runner import ImageRunner
from openstackquery.time_utils import TimeUtils


class ImageMapping(MappingInterface):
    """
    Mapping class for querying Openstack Image objects.
    Define property mappings, kwarg mappings and filter function mappings, and runner mapping related to images here
    """

    @staticmethod
    def get_chain_mappings() -> QueryChainMappings:
        """
        Return a dictionary containing property pairs mapped to query mappings.
        This is used to define how to chain results from this query to other possible queries
        """
        return {ImageProperties.IMAGE_ID: [ServerProperties.IMAGE_ID]}

    @staticmethod
    def get_runner_mapping() -> Type[ImageRunner]:
        """
        Returns a mapping to associated Runner class for the Query (ImageRunner)
        """
        return ImageRunner

    @staticmethod
    def get_prop_mapping() -> Type[ImageProperties]:
        """
        Returns a mapping of valid presets for server side attributes (ImageProperties)
        """
        return ImageProperties

    @staticmethod
    def get_server_side_handler() -> ServerSideHandler:
        """
        method to configure a server handler which can be used to get 'filter' keyword arguments that
        can be passed to openstack function conn.compute.images() to filter results for a valid preset-property pair

        valid filters documented here:
            https://docs.openstack.org/openstacksdk/latest/user/proxies/compute.html
            https://docs.openstack.org/api-ref/image/v2/index.html#list-images
        """
        return ServerSideHandler(
            {
                QueryPresets.EQUAL_TO: {
                    ImageProperties.IMAGE_NAME: lambda value: {"name": value},
                    ImageProperties.IMAGE_STATUS: lambda value: {"status": value},
                },
                QueryPresets.ANY_IN: {
                    ImageProperties.IMAGE_NAME: lambda values: [
                        {"name": value} for value in values
                    ],
                    ImageProperties.IMAGE_STATUS: lambda values: [
                        {"status": value} for value in values
                    ],
                },
                QueryPresets.OLDER_THAN: {
                    ImageProperties.IMAGE_CREATION_DATE: lambda func=TimeUtils.convert_to_timestamp, **kwargs: {
                        "created_at": f"lt:{func(**kwargs)}"
                    },
                    ImageProperties.IMAGE_LAST_UPDATED_DATE: lambda func=TimeUtils.convert_to_timestamp, **kwargs: {
                        "updated_at": f"lt:{func(**kwargs)}"
                    },
                },
                QueryPresets.OLDER_THAN_OR_EQUAL_TO: {
                    ImageProperties.IMAGE_CREATION_DATE: lambda func=TimeUtils.convert_to_timestamp, **kwargs: {
                        "created_at": f"lte:{func(**kwargs)}"
                    },
                    ImageProperties.IMAGE_LAST_UPDATED_DATE: lambda func=TimeUtils.convert_to_timestamp, **kwargs: {
                        "updated_at": f"lte:{func(**kwargs)}"
                    },
                },
                QueryPresets.YOUNGER_THAN: {
                    ImageProperties.IMAGE_CREATION_DATE: lambda func=TimeUtils.convert_to_timestamp, **kwargs: {
                        "created_at": f"gt:{func(**kwargs)}"
                    },
                    ImageProperties.IMAGE_LAST_UPDATED_DATE: lambda func=TimeUtils.convert_to_timestamp, **kwargs: {
                        "updated_at": f"gt:{func(**kwargs)}"
                    },
                },
                QueryPresets.YOUNGER_THAN_OR_EQUAL_TO: {
                    ImageProperties.IMAGE_CREATION_DATE: lambda func=TimeUtils.convert_to_timestamp, **kwargs: {
                        "created_at": f"gte:{func(**kwargs)}"
                    },
                    ImageProperties.IMAGE_LAST_UPDATED_DATE: lambda func=TimeUtils.convert_to_timestamp, **kwargs: {
                        "updated_at": f"gte:{func(**kwargs)}"
                    },
                },
                QueryPresets.GREATER_THAN_OR_EQUAL_TO: {
                    ImageProperties.IMAGE_SIZE: lambda value: {"size_min": int(value)}
                },
                QueryPresets.LESS_THAN_OR_EQUAL_TO: {
                    ImageProperties.IMAGE_SIZE: lambda value: {"size_max": int(value)}
                },
            }
        )

    @staticmethod
    def get_client_side_handler() -> ClientSideHandler:
        """
        This function returns a client-side handler object which can be used to handle filtering results locally.
        This function maps which properties are valid for each filter preset.
        """
        integer_prop_list = [
            ImageProperties.IMAGE_SIZE,
            ImageProperties.IMAGE_MINIMUM_RAM,
            ImageProperties.IMAGE_MINIMUM_DISK,
            ImageProperties.IMAGE_CREATION_PROGRESS,
        ]
        date_prop_list = [
            ImageProperties.IMAGE_CREATION_DATE,
            ImageProperties.IMAGE_LAST_UPDATED_DATE,
        ]

        return ClientSideHandler(
            {
                QueryPresets.EQUAL_TO: ["*"],
                QueryPresets.NOT_EQUAL_TO: ["*"],
                QueryPresets.ANY_IN: ["*"],
                QueryPresets.NOT_ANY_IN: ["*"],
                QueryPresets.MATCHES_REGEX: [ImageProperties.IMAGE_NAME],
                QueryPresets.YOUNGER_THAN: date_prop_list,
                QueryPresets.YOUNGER_THAN_OR_EQUAL_TO: date_prop_list,
                QueryPresets.OLDER_THAN: date_prop_list,
                QueryPresets.OLDER_THAN_OR_EQUAL_TO: date_prop_list,
                QueryPresets.LESS_THAN: integer_prop_list,
                QueryPresets.LESS_THAN_OR_EQUAL_TO: integer_prop_list,
                QueryPresets.GREATER_THAN: integer_prop_list,
                QueryPresets.GREATER_THAN_OR_EQUAL_TO: integer_prop_list,
            }
        )
