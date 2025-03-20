import sys
import logging
from openstackquery.api.query_objects import (
    ServerQuery,
    UserQuery,
    FlavorQuery,
    ProjectQuery,
    ImageQuery,
    HypervisorQuery,
)

# Create logger
openstack_query_loggers = logging.getLogger(__name__)

# Create Handler for logging data to stderr
logger_handler = logging.StreamHandler(sys.stderr)

# Create a Formatter for formatting the log messages
logger_formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")

# Add the Formatter to the Handler
logger_handler.setFormatter(logger_formatter)

# Add the Handler to the Logger
openstack_query_loggers.addHandler(logger_handler)

# don't propagate error logs to avoid duplication
openstack_query_loggers.propagate = False
