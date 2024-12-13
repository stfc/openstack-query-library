# Flavors
Flavors refer to Openstack Compute Flavors. Flavors define the compute, memory, and storage capacity of nova computing instances.
See [Openstack Docs](https://docs.openstack.org/api-ref/compute/#flavors) for more info

**NOTE: `FlavorQuery` will only work with admin credentials - set by `clouds.yaml`**

## Querying

To Query for Flavors using the Query Library, you can import `FlavorQuery()` like so:

```python
from openstackquery import FlavorQuery
```

`FlavorQuery()` can then be used to setup and run queries - see [API.md](../API.md) for details on API calls

## Properties

Each `Flavor` has the following properties

| Return Type | Property Name(s) (case-insensitive)                  | Description                                                                                     |
|-------------|------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| `string`    | "description", "desc"                                | The description of the flavor                                                                   |
| `int`       | "disk", "disk_size"                                  | Size of the disk this flavor offers. Type: int                                                  |
| `int`       | "ephemeral", "ephemeral_disk", "ephemeral_disk_size" | Size of the ephemeral data disk attached to this server. Type: int                              |
| `string`    | "id", "uuid"                                         | Unique ID Openstack has assigned the flavor.                                                    |
| `bool`      | "is_disabled"                                        | Indicates whether flavor is disabled. <br/>True if disabled, False if not                       |
| `bool`      | "is_public"                                          | Indicates if flavor is available to all projects. <br/>True if publicly available, False if not |
| `string`    | "name"                                               | Name of the flavor                                                                              |
| `int`       | "ram", "ram_size                                     | The amount of RAM (in MB) this flavor offers. Type: int                                         |
| `int`       | "swap", "swap_size"                                  | Size of the swap partitions.                                                                    |
| `int`       | "vcpu", "vcpus"                                      | The number of virtual CPUs this flavor offers. Type: int                                        |

Any of these properties can be used for any of the API methods that takes a property - like `select`, `where`, `sort_by` etc

## Chaining
This section details valid mappings you can use to chain onto other queries or from other queries to chain into a `FlavorQuery` object.
This applies to API calls `then` and `append_from` - see [API.md](../API.md) for details

## Query Alias
The aliases that can be used for the query when chaining are listed below:

| Aliases (case-insensitive)                         |
|----------------------------------------------------|
| "flavor", "flavors", "flavor_query", "flavorquery" |



## Chaining from
A `FlavorQuery` can be chained to other queries.
The following shared-common properties are listed below (as well as the Query object they map to):

| Prop 1 | Prop 2        | Type        | Maps                           | Documentation            |
|--------|---------------|-------------|--------------------------------|--------------------------|
| `"id"` | `"flavor_id"` | One-to-Many | `FlavorQuery` to `ServerQuery` | [SERVERS.md](SERVERS.md) |


## Chaining to
Chaining from other `FlavorQuery` requires passing `flavor_query` or any aliases mentioned above as the `query_type`

| From          | Prop 1        | Prop 2 | Type        | Documentation            |
|---------------|---------------|--------|-------------|--------------------------|
| `ServerQuery` | `"flavor_id"` | `"id"` | Many-to-One | [SERVERS.md](SERVERS.md) |


## run() meta-parameters

`FlavorQuery()` accepts no extra meta-parameters when calling `run()`
