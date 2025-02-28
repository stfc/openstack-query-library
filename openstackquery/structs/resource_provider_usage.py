from dataclasses import dataclass


# pylint: disable=too-many-instance-attributes
@dataclass
class ResourceProviderUsage:
    """
    Upstream has a resource provider class which only provides available resources.
    Current usage is not supported at all. Instead, create a custom class to store
    usage and total information until upstream updates its resource provider class.
    """

    vcpus_avail: int
    memory_mb_avail: int
    disk_gb_avail: int

    vcpus: int
    memory_mb_size: int
    disk_gb_size: int

    vcpus_used: int
    memory_mb_used: int
    disk_gb_used: int
