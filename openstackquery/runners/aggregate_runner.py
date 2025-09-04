import logging
from typing import List, Optional

from openstack.compute.v2.aggregate import Aggregate

from openstackquery.aliases import OpenstackResourceObj, ServerSideFilter
from openstackquery.openstack_connection import OpenstackConnection
from openstackquery.runners.runner_wrapper import RunnerWrapper

logger = logging.getLogger(__name__)


class AggregateRunner(RunnerWrapper):
    """
    Runner class for openstack Aggregate resource
    AggregateRunner encapsulates running any openstacksdk Aggregate commands
    """

    RESOURCE_TYPE = Aggregate

    def parse_meta_params(self, conn: OpenstackConnection, **kwargs):
        """
        This method is a helper function that will parse a set of meta params specific to the resource and
        return a set of parsed meta-params to pass to _run_query
        """
        logger.debug("AggregateQuery has no meta-params available")
        return super().parse_meta_params(conn, **kwargs)

    def run_query(
        self,
        conn: OpenstackConnection,
        filter_kwargs: Optional[ServerSideFilter] = None,
        **kwargs,
    ) -> List[OpenstackResourceObj]:
        """
        This method runs the query by running openstacksdk commands

        For AggregateQuery, this command finds all aggregates that match a given set of filter_kwargs
        :param conn: An OpenstackConnection object - used to connect to openstacksdk
        :param filter_kwargs: An Optional list of filter kwargs to pass to conn.identity.aggregates()
            to limit the hypervisors being returned.
            - see https://docs.openstack.org/api-ref/compute/?expanded=list-hypervisors-detail#list-aggregates
        """
        if not filter_kwargs:
            # return server info
            filter_kwargs = {}
        logger.debug(
            "running openstacksdk command conn.compute.aggregates(%s)",
            ",".join(f"{key}={value}" for key, value in filter_kwargs.items()),
        )

        # Note: Pagination isn't supported by the API,
        # as the `marker` and `limit` properties don't exist for list aggregates
        return conn.compute.aggregates(**filter_kwargs)
