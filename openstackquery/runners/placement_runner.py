import logging
from typing import List, Optional, Dict

from openstack import exceptions, utils
from openstack.placement.v1.resource_provider import ResourceProvider

from openstackquery.aliases import (
    OpenstackResourceObj,
    ServerSideFilter,
)
from openstackquery.openstack_connection import OpenstackConnection
from openstackquery.runners.runner_wrapper import RunnerWrapper
from openstackquery.structs.resource_provider_usage import ResourceProviderUsage

logger = logging.getLogger(__name__)


class PlacementRunner(RunnerWrapper):
    """
    Runner class for openstack Hypervisor resource
    HypervisorRunner encapsulates running any openstacksdk Hypervisor commands
    """

    RESOURCE_TYPE = ResourceProvider

    def parse_meta_params(self, conn: OpenstackConnection, **kwargs) -> Dict[str, str]:
        """
        Placement runner has no meta-params available
        """
        logger.debug("PlacementQuery has no meta-params available")
        return super().parse_meta_params(conn, **kwargs)

    def _convert_to_custom_obj(
        self, conn: OpenstackConnection, obj: ResourceProvider
    ) -> OpenstackResourceObj:
        """
        Converts an openstacksdk ResourceProvider object to a ResourceProviderUsage object
        including populating the available and used resources from the placement API
        :param conn: Openstack connection
        :param obj: Openstack placement resource provider object
        :return: A ResourceProviderUsage object
        """
        usage = self._get_usage_info(conn, obj)
        avail = self._get_availability_info(conn, obj)
        return ResourceProviderUsage(
            id=obj.id,
            name=obj.name,
            vcpu_used=usage["VCPU"],
            memory_mb_used=usage["MEMORY_MB"],
            disk_gb_used=usage["DISK_GB"],
            vcpu_avail=avail["VCPU"],
            memory_mb_avail=avail["MEMORY_MB"],
            disk_gb_avail=avail["DISK_GB"],
        )

    @staticmethod
    def _get_availability_info(
        conn: OpenstackConnection, resource_provider_obj: ResourceProvider
    ) -> Dict:
        """
        Gets availability stats for a given placement resource provider
        across the following resource classes: VCPU, MEMORY_MB, DISK_GB
        :param conn: Openstack connection
        :param resource_provider_obj: Openstack placement resource provider object
        :return: A dictionary with the summed availability stats using the class name as a key
        """
        summed_classes = {}
        for resource_class in ["VCPU", "MEMORY_MB", "DISK_GB"]:
            placement_inventories = conn.placement.resource_provider_inventories(
                resource_provider_obj, resource_class=resource_class
            )
            # A resource provider can have n number of inventories for a given resource class
            if not placement_inventories:
                logger.warning(
                    "No available resources found for resource provider: %s",
                    resource_provider_obj.id,
                )
                summed_classes[resource_class] = 0
            else:
                summed_classes[resource_class] = sum(
                    i["total"] for i in placement_inventories
                )
        return summed_classes

    @staticmethod
    def _get_usage_info(
        conn: OpenstackConnection, resource_provider_obj: ResourceProvider
    ) -> Dict:
        """
        Gets usage stats for a given placement resource provider
        :param conn: Openstack connection
        :param resource_provider_obj: Openstack placement resource provider object
        :return: A ResourceProviderUsage object with usage stats
        """
        # The following should be up-streamed to openstacksdk at some point
        # It is based on the existing `resource_provider.py:fetch_aggregates` method
        # found in the OpenStack SDK
        url = utils.urljoin(
            ResourceProvider.base_path, resource_provider_obj.id, "usages"
        )

        response = conn.session.get(url, endpoint_filter={"service_type": "placement"})
        exceptions.raise_from_response(response)
        return response.json()["usages"]

    # pylint: disable=unused-argument
    def run_query(
        self,
        conn: OpenstackConnection,
        filter_kwargs: Optional[ServerSideFilter] = None,
        **kwargs,
    ) -> List[OpenstackResourceObj]:
        """
        This method runs the query by running openstacksdk placement commands

        :param conn: An OpenstackConnection object - used to connect to openstacksdk
        :param filter_kwargs: An Optional list of filter kwargs to pass to the openstacksdk command
        """
        logger.debug(
            "running openstacksdk command conn.placement.resource_providers(%s)",
            ",".join(f"{key}={value}" for key, value in filter_kwargs.items()),
        )
        resource_providers = conn.placement.resource_providers(**filter_kwargs)
        return [
            self._convert_to_custom_obj(conn, provider)
            for provider in resource_providers
        ]
