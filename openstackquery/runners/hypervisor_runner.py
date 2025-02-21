import logging
from typing import List, Optional, Dict

from openstack import exceptions, utils
from openstack.compute.v2.hypervisor import Hypervisor as OpenstackHypervisor
from openstack.placement.v1.resource_provider import ResourceProvider

from openstackquery.aliases import OpenstackResourceObj, ServerSideFilters
from openstackquery.openstack_connection import OpenstackConnection
from openstackquery.runners.runner_utils import RunnerUtils
from openstackquery.runners.runner_wrapper import RunnerWrapper

from openstackquery.structs.hypervisor import Hypervisor
from openstackquery.structs.resource_provider_usage import ResourceProviderUsage

logger = logging.getLogger(__name__)


class HypervisorRunner(RunnerWrapper):
    """
    Runner class for openstack Hypervisor resource
    HypervisorRunner encapsulates running any openstacksdk Hypervisor commands
    """

    RESOURCE_TYPE = OpenstackHypervisor

    def parse_meta_params(self, conn: OpenstackConnection, **kwargs):
        """
        This method is a helper function that will parse a set of meta params specific to the resource and
        return a set of parsed meta-params to pass to _run_query
        :param conn: An OpenstackConnection object - used to connect to openstack and parse meta params
        """
        logger.debug("HypervisorQuery has no meta-params available")
        return super().parse_meta_params(conn, **kwargs)

    def get_hv_usage_data(
        self,
        conn: OpenstackConnection,
    ) -> Dict:
        """
        collects usage data for hypervisors using the placement API
        :param conn: Openstack connection
        :return: A ResourceProviderUsage object
        """
        logger.debug(
            "running openstacksdk command conn.placement.resource_providers()",
        )
        resource_providers = conn.placement.resource_providers()
        return {
            provider["name"]: self._convert_to_custom_obj(conn, provider)
            for provider in resource_providers
        }

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

        vcpu_used = usage.get("VCPU", 0)
        memory_mb_used = usage.get("MEMORY_MB", 0)
        disk_gb_used = usage.get("DISK_GB", 0)

        return ResourceProviderUsage(
            # workaround for hvs not containing VCPU/Memory/Disk resource provider info - set to 0
            vcpu_used=vcpu_used,
            memory_mb_used=memory_mb_used,
            disk_gb_used=disk_gb_used,
            vcpu_avail=avail["VCPU"],
            memory_mb_avail=avail["MEMORY_MB"],
            disk_gb_avail=avail["DISK_GB"],
            vcpus=avail["VCPU"] + vcpu_used,
            memory_mb_size=avail["MEMORY_MB"] + memory_mb_used,
            disk_gb_size=avail["DISK_GB"] + disk_gb_used,
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
                    resource_provider_obj["id"],
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
            ResourceProvider.base_path, resource_provider_obj["id"], "usages"
        )
        response = conn.session.get(url, endpoint_filter={"service_type": "placement"})
        exceptions.raise_from_response(response)
        return response.json()["usages"]

    # pylint: disable=unused-argument
    def run_query(
        self,
        conn: OpenstackConnection,
        filter_kwargs: Optional[ServerSideFilters] = None,
        **kwargs,
    ) -> List[Hypervisor]:
        """
        This method runs the query by running openstacksdk commands

        For HypervisorQuery, this command finds all hypervisors that match a given set of filter_kwargs
        :param conn: An OpenstackConnection object - used to connect to openstacksdk
        :param filter_kwargs: An Optional list of filter kwargs to pass to conn.compute.hypervisors()
            to limit the hypervisors being returned.
            - see https://docs.openstack.org/api-ref/compute/?expanded=list-hypervisors-detail
        """
        if not filter_kwargs:
            # return server info
            filter_kwargs = {"details": True}
        logger.debug(
            "running openstacksdk command conn.compute.hypervisors(%s)",
            ",".join(f"{key}={value}" for key, value in filter_kwargs.items()),
        )
        hvs = RunnerUtils.run_paginated_query(
            conn.compute.hypervisors, self._page_marker_prop_func, filter_kwargs
        )
        usage_data = self.get_hv_usage_data(conn)
        return [Hypervisor(hv=hv, usage=usage_data.get(hv["name"], None)) for hv in hvs]
