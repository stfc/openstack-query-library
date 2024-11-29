from openstack.connection import Connection
from openstack import connect


class OpenstackConnection:
    """
    Wraps an openstack connection as a context manager.
    This class is used as follows:
        with(OpenstackConnection()) as <name>:
            name.<openstack_api>.method()
    """

    def __init__(self, cloud_name: str):
        """
        Starts a connection with the Openstack API when used in a context manager
        :param cloud_name: The name of the cloud found in clouds.yaml
        """
        self._cloud_name = cloud_name.strip() if cloud_name else None
        self._connection = None

    def __enter__(self) -> Connection:
        if not self._cloud_name:
            # If we don't provide a cloud name (or an empty one), Openstack will
            # default to env vars, which may be a security problem if they are incorrectly set
            raise RuntimeError("A cloud name is required but was not provided.")
        self._connection = connect(cloud=self._cloud_name)
        return self._connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()
        self._connection = None
