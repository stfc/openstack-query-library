from dataclasses import dataclass


# pylint: disable=too-many-instance-attributes
@dataclass
class ResourceProviderUsage:
    """
    Upstream has a resource provider class which only provides available resources.
    Current usage is not supported at all. Instead, create a custom class to store
    usage and total information until upstream updates its resource provider class.
    """

    # Lower case to maintain compatibility with existing ResourceProvider object
    name: str
    id: str

    vcpu_avail: int
    memory_mb_avail: int
    disk_gb_avail: int

    vcpu_used: int
    memory_mb_used: int
    disk_gb_used: int
