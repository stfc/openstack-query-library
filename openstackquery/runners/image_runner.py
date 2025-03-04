from typing import Optional, List, Dict
import logging

from openstack.compute.v2.image import Image

from openstackquery.openstack_connection import OpenstackConnection
from openstackquery.runners.runner_utils import RunnerUtils
from openstackquery.runners.runner_wrapper import RunnerWrapper

from openstackquery.exceptions.parse_query_error import ParseQueryError
from openstackquery.aliases import ServerSideFilter, ProjectIdentifier

logger = logging.getLogger(__name__)


class ImageRunner(RunnerWrapper):
    """
    Runner class for openstack image resource
    ImageRunner encapsulated running any openstacksdk Image commands
    """

    RESOURCE_TYPE = Image

    def parse_meta_params(
        self,
        conn: OpenstackConnection,
        from_projects: Optional[List[ProjectIdentifier]] = None,
        all_projects: bool = False,
        as_admin: bool = False,
        **_,
    ) -> Dict:
        """
        This method is a helper function that will parse a set of meta params specific to the resource and
        return a set of parsed meta-params to pass to _run_query
        :param conn: An OpenstackConnection object - used to connect to openstack and parse meta params
        :param from_projects: A list of projects to search in
        :param all_projects: A boolean which, if true - will run query on all available projects to the user
        :param as_admin: A boolean which, if true - will run query as an admin
        """
        # raise error if ambiguous query
        if from_projects and all_projects:
            raise ParseQueryError(
                "Failed to execute query: ambiguous run params - run with either "
                "from_projects or all_projects and not both"
            )

        if not as_admin and all_projects:
            raise ParseQueryError(
                "Failed to execute query: run_params given won't work if "
                "you're not running as admin"
            )

        if all_projects:
            return {}

        if not from_projects:
            logger.warning(
                "Query will only work on the scoped project id: %s",
                conn.current_project_id,
            )
            from_projects = [conn.current_project_id]

        projects = RunnerUtils.parse_projects(conn, from_projects)

        return {"projects": projects}

    def run_query(
        self,
        conn: OpenstackConnection,
        filter_kwargs: Optional[ServerSideFilter] = None,
        **meta_params,
    ) -> List[Image]:
        """
        This method runs the query by running openstacksdk commands

        For ImageQuery, this command finds all images that match a given set of filter_kwargs.
        If meta-param from_projects passed, it will limit search to images that belong to those projects only
        :param conn: An OpenstackConnection object - used to connect to openstacksdk
        :param filter_kwargs: An Optional set of filter kwargs to pass to conn.compute.images()
            to limit the images being returned.
            see https://docs.openstack.org/api-ref/image/v2/index.html#list-images
        :param meta_params: a set of meta parameters that dictates how the query is run
        """
        if not filter_kwargs:
            filter_kwargs = {}

        if "projects" not in meta_params:
            return RunnerUtils.run_paginated_query(
                conn.compute.images, self._page_marker_prop_func, dict(filter_kwargs)
            )
        query_res = []
        project_num = len(meta_params["projects"])
        logger.debug("running query on %s projects", project_num)
        for i, project_id in enumerate(meta_params["projects"], 1):
            filter_kwargs.update({"owner": project_id})
            logger.debug(
                "running query on project %s / %s (id: %s)", i, project_num, project_id
            )
            logger.debug(
                "running openstacksdk command conn.compute.images (%s)",
                ", ".join(f"{key}={value}" for key, value in filter_kwargs.items()),
            )
            query_res.extend(
                RunnerUtils.run_paginated_query(
                    conn.compute.images,
                    self._page_marker_prop_func,
                    dict(filter_kwargs),
                )
            )
        return query_res
