from unittest.mock import patch

import pytest
from openstackquery.openstack_connection import OpenstackConnection


@patch("openstackquery.openstack_connection.connect")
def test_openstack_connection_connects_first_time(patched_connect):
    """
    Tests that connect it correctly called on entry.
    Does not check the args passed to connect
    """
    with OpenstackConnection("a") as instance:
        patched_connect.assert_called_once()
        assert instance == patched_connect.return_value


@patch("openstackquery.openstack_connection.connect")
def test_openstack_connection_uses_cloud_name(patched_connect):
    """
    Tests that the cloud name gets used in the call to connect correctly
    """
    expected_cloud = "foo"

    with OpenstackConnection(expected_cloud):
        patched_connect.assert_called_once_with(cloud=expected_cloud)


def test_connection_throws_for_no_cloud_name():
    """
    Tests a None type will throw if used as the account name
    """
    with pytest.raises(RuntimeError):
        with OpenstackConnection(None):
            pass


@patch("openstackquery.openstack_connection.connect")
def test_connection_throws_for_empty_cloud_name(_):
    """
    Tests an empty string will throw for the cloud name
    """
    with pytest.raises(RuntimeError):
        with OpenstackConnection(""):
            pass


@patch("openstackquery.openstack_connection.connect")
def test_connection_throws_for_whitespace_cloud_name(_):
    """
    Tests a whitespace string will throw for the cloud name
    """
    with pytest.raises(RuntimeError):
        with OpenstackConnection(" \t"):
            pass


@patch("openstackquery.openstack_connection.connect")
def test_openstack_connection_disconnects(patched_connect):
    """
    Checks the session is correctly closed (to not leak handles)
    when the context manager exits
    """
    with OpenstackConnection("a") as instance:
        connection_handle = patched_connect.return_value
        assert instance == connection_handle
    connection_handle.close.assert_called_once()


@patch("openstackquery.openstack_connection.connect")
def test_openstack_connection_connects_second_time(patched_connect):
    """
    Tests that creating two connections calls connect twice.
    Why, because Singletons are evil and cause nothing but problems
    """
    with OpenstackConnection("a"):
        pass
    with OpenstackConnection("a"):
        pass
    assert patched_connect.call_count == 2
