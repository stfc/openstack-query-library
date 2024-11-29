import logging
from typing import Optional, Dict, List

from openstack.identity.v3.user import User
from openstackquery.openstack_connection import OpenstackConnection
from openstackquery.runners.runner_utils import RunnerUtils
from openstackquery.runners.runner_wrapper import RunnerWrapper

from openstackquery.aliases import ServerSideFilter

logger = logging.getLogger(__name__)


class UserRunner(RunnerWrapper):
    """
    Runner class for openstack User resource.
    UserRunner encapsulates running any openstacksdk User commands
    """

    RESOURCE_TYPE = User

    def parse_meta_params(
        self, conn: OpenstackConnection, from_domain: str = "default", **_
    ) -> Dict:
        """
        This method is a helper function that will parse a set of query meta params related to openstack user queries
        :param conn: An OpenstackConnection object - used to connect to openstack and parse meta params
        :param from_domain: (optional) name of which user domain to search in ("default" if not given)
        """
        logger.info("searching in user domain: '%s'", from_domain)
        return {"domain_id": conn.identity.find_domain(from_domain)["id"]}

    def run_query(
        self,
        conn: OpenstackConnection,
        filter_kwargs: Optional[ServerSideFilter] = None,
        **meta_params,
    ) -> List[Optional[User]]:
        """
        This method runs the query by running openstacksdk commands

        For UserQuery, this command gets all users by domain ID
        :param conn: An OpenstackConnection object - used to connect to openstacksdk
        :param filter_kwargs: An Optional set of filter kwargs to pass to conn.identity.users()
        """

        if not filter_kwargs:
            filter_kwargs = {}

        # having a filter of 'id' - will automatically mean no other filter kwargs
        selected_id = filter_kwargs.get("id", None)
        if selected_id:
            val = conn.identity.find_user(selected_id, ignore_missing=True)
            return [val] if val else []

        filter_kwargs.update({"domain_id": meta_params["domain_id"]})

        logger.debug(
            "searching for users using domain_id: '%s'", filter_kwargs["domain_id"]
        )

        logger.debug(
            "running paginated openstacksdk command conn.identity.users (%s)",
            ",".join(f"{key}={value}" for key, value in filter_kwargs.items()),
        )
        return RunnerUtils.run_paginated_query(
            conn.identity.users, self._page_marker_prop_func, filter_kwargs
        )
