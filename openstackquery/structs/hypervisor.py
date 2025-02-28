from dataclasses import dataclass

from openstack.compute.v2.hypervisor import Hypervisor as OpenstackHypervisor
from structs.resource_provider_usage import ResourceProviderUsage


# pylint: disable=too-many-instance-attributes
@dataclass
class Hypervisor:
    """
    A dataclass that wraps an openstacksdk "hypervisor" object its corresponding resource provider usage object
    allows hv data and hv usage data to be outputted from one hypervisor query
    """

    hv: OpenstackHypervisor
    usage: ResourceProviderUsage
