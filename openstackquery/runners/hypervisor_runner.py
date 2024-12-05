import json
import logging
from typing import Dict, List, Optional

from openstack.compute.v2.hypervisor import Hypervisor
from osc_placement.http import SessionClient as PlacementClient

from openstackquery.aliases import OpenstackResourceObj, ServerSideFilters
from openstackquery.openstack_connection import OpenstackConnection
from openstackquery.runners.runner_utils import RunnerUtils
from openstackquery.runners.runner_wrapper import RunnerWrapper

logger = logging.getLogger(__name__)


class HypervisorRunner(RunnerWrapper):
    """
    Runner class for openstack Hypervisor resource
    HypervisorRunner encapsulates running any openstacksdk Hypervisor commands
    """

    RESOURCE_TYPE = Hypervisor

    def parse_meta_params(self, conn: OpenstackConnection, **kwargs):
        """
        This method is a helper function that will parse a set of meta params specific to the resource and
        return a set of parsed meta-params to pass to _run_query
        """
        logger.debug("HypervisorQuery has no meta-params available")
        return super().parse_meta_params(conn, **kwargs)

    def _populate_placement_info(
        self, conn: OpenstackConnection, hypervisors: List
    ) -> List:
        """
        Adds resource usage stats to the hypervisors
        :param conn: Openstack connecion
        :param hypervisors: List of hypervisors
        :return: List of hypervisors with additional resource usage stats
        """
        client = PlacementClient(
            api_version="1.6",
            session=conn.session,
            ks_filter={"service_type": "placement"},
        )

        for hypervisor in hypervisors:
            hypervisor.resources = self._get_usage_info(conn, client, hypervisor)

        return hypervisors

    def _get_usage_info(
        self, conn: OpenstackConnection, client: PlacementClient, hypervisor: Hypervisor
    ) -> Dict:
        """
        Get usage stats from the openstack placement api
        :param conn: Openstack connection
        :param client: osc_placement session client
        :param hypervisor: Openstack hypervisor
        :return: resource usage for the hypervisor
        """
        resources = conn.placement.resource_provider_inventories(hypervisor.id)
        usages = client.request("get", f"/resource_providers/{hypervisor.id}/usages")
        usages = json.loads(usages.text).get("usages")
        usage_info = {}
        for i in resources:
            usage_info[i.resource_class] = {
                "total": i.total,
                "usage": usages.get(i.resource_class),
                "free": i.total - usages.get(i.resource_class),
            }

        return usage_info

    # pylint: disable=unused-argument
    def run_query(
        self,
        conn: OpenstackConnection,
        filter_kwargs: Optional[ServerSideFilters] = None,
        **kwargs,
    ) -> List[OpenstackResourceObj]:
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
        hypervisors = RunnerUtils.run_paginated_query(
            conn.compute.hypervisors, self._page_marker_prop_func, filter_kwargs
        )

        return self._populate_placement_info(conn, hypervisors)
