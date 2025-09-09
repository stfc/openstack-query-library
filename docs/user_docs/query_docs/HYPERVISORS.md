# Hypervisors
Hypervisors refer to the software that creates and runs virtual machines (VMs) (Also known in Openstack as Servers).
The physical device the Hypervisor runs on is known as the host.
See [Openstack Docs](https://docs.openstack.org/api-ref/compute/#hypervisors-os-hypervisors) for more info

**NOTE: `HypervisorQuery` will only work with admin credentials - set by `clouds.yaml`**

## Querying

To Query for Hypervisors using the Query Library, you can import `HypervisorQuery()` like so:

```python
from openstackquery import HypervisorQuery
```

`HypervisorQuery()` can then be used to setup and run queries - see [API.md](../API.md) for details on API calls

## Properties

`Hypervisors` have the following properties:

| Return Type | Property Name(s) (case-insensitive)                              | Description                                                     |
|-------------|------------------------------------------------------------------|-----------------------------------------------------------------|
| `int`       | "disk_gb_avail", "disk_avail", "local_disk_free", "free_disk_gb" | The local disk space remaining on this hypervisor(in GiB)       |
| `int`       | "disk_gb_used", "disk_used", "local_disk_used", "local_gb_used"  | The local disk space allocated on this hypervisor(in GiB)       |
| `int`       | "disk_gb_size", "disk", "local_disk", "local_gb"                 | The total amount of local disk space(in GiB)                    |
| `string`    | "id", "uuid", "host_id"                                          | ID of the Hypervisor                                            |
| `string`    | "ip", "host_ip"                                                  | The IP address of the hypervisor’s host                         |
| `int`       | "memory_mb_avail", "memory_avail", "memory_free", "free_ram_mb"  | The free RAM on this hypervisor(in MiB).                        |
| `int`       | "memory_used", "memory_mb_used"                                  | RAM currently being used on this hypervisor(in MiB).            |
| `int`       | "memory_mb_size", "memory_size", "memory_mb", "memory", "ram"    | The total amount of ram(in MiB)                                 |
| `string`    | "name", "host_name"                                              | Hypervisor Hostname                                             |
| `string`    | "state"                                                          | The state of the hypervisor. One of up or down.                 |
| `string`    | "status"                                                         | The status of the hypervisor. One of enabled or disabled.       |
| `int`       | "vcpus"                                                          | The number of vCPUs on this hypervisor.                         |
| `int`       | "vcpus_free" "vcpus_avail"                                       | The number of vCPUs on this hypervisor.                         |
| `int`       | "vcpus_used", "vcpus_in_use"                                     | The number of vCPUs currently being used on this hypervisor.    |
| `string`    | "disabled_reason"                                                | Comment of why the hypervisor is disabled, None if not disabled |
| `float`     | "uptime"                                                         | The total uptime in days of the hypervisor                      |

Any of these properties can be used for any of the API methods that takes a property - like `select`, `where`, `sort_by` etc

## Chaining
This section details valid mappings you can use to chain onto other queries or from other queries to chain into a `HypervisorQuery` object.
This applies to API calls `then` and `append_from` - see [API.md](../API.md) for details

## Query Alias
The aliases that can be used for the query when chaining are listed below:

| Aliases (case-insensitive                                          |
|--------------------------------------------------------------------|
| "hypervisor", "hypervisors", "hypervisor_query", "hypervisorquery" |



## Chaining from
A `HypervisorQuery` can be chained to other queries.
The following shared-common properties are listed below (as well as the Query object they map to):

| Prop 1 | Prop 2            | Type        | Maps                                | Documentation            |
|--------|-------------------|-------------|-------------------------------------|--------------------------|
| "name" | "hypervisor_name" | One-to-Many | `HypervisorQuery` to `ServerQuery`  | [SERVERS.md](SERVERS.md) |


## Chaining to
Chaining from other `HypervisorQuery` requires passing `hypervisor_query` or any aliases mentioned above as the `query_type`

| From          | Prop 1            | Prop 2 | Type        | Documentation            |
|---------------|-------------------|--------|-------------|--------------------------|
| `ServerQuery` | "hypervisor_name" | "name" | Many-to-One | [SERVERS.md](SERVERS.md) |


## run() meta-parameters

`HypervisorQuery()` accepts no extra meta-parameters when calling `run()`
