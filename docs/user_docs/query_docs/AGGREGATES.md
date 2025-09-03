# Aggregates

Aggregates refer to **Host Aggregates** in OpenStack. These are logical groupings of compute hosts with shared metadata. They're typically used for scheduling decisions (e.g., grouping GPU hosts or separating workloads).

See [OpenStack Docs](https://docs.openstack.org/api-ref/compute/#host-aggregates-os-aggregates) for more info.

**NOTE: `AggregateQuery` will only work with admin credentials - set by `clouds.yaml`**

---

## Querying

To query for Aggregates using the Query Library, you can import `AggregateQuery()` like so:

```
from openstackquery import AggregateQuery
```

`AggregateQuery()` can then be used to setup and run queries - see [API.md](../API.md) for details on API calls.

---

## Properties

Each `Aggregate` has the following properties:

| Return Type | Property Name(s) (case-insensitive)                      | Description                                                                       |
|-------------|----------------------------------------------------------|-----------------------------------------------------------------------------------|
| `string`    | "created_at"                                             | Timestamp the aggregate was created. Format: ISO8601                              |
| `bool`      | "deleted"                                                | Boolean indicating whether the aggregate has been deleted                         |
| `string`    | "deleted_at"                                             | Timestamp the aggregate was deleted, if applicable. Format: ISO8601               |
| `int`       | "metadata_gpunum", "gpunum"                              | Number of GPUs associated with this aggregate (from metadata key `gpunum`)        |
| `string`    | "hosts", "host_ips"                                      | List of hosts in the aggregate (as a JSON-formatted string)                       |
| `string`    | "metadata_hosttype", "hosttype"                          | Host type value (from metadata key `hosttype`)                                    |
| `string`    | "metadata_local_storage_type", "local_storage_type"      | Local storage type (from metadata key `local-storage-type`)                       |
| `string`    | "metadata"                                               | Full metadata dictionary (as JSON-formatted string)                               |
| `string`    | "updated_at"                                             | Timestamp the aggregate was last updated. Format: ISO8601                         |
| `string`    | "id", "uuid"                                             | Unique ID of the aggregate (UUID)                                                 |

Any of these properties can be used for any of the API methods that take a property - like `select`, `where`, `sort_by`, etc.

---

## Chaining

This section details valid mappings you can use to chain onto other queries or from other queries to chain into an `AggregateQuery` object.

This applies to API calls `then` and `append_from` - see [API.md](../API.md) for details.

---

## Query Alias

The aliases that can be used for the query when chaining are listed below:

| Aliases (case-insensitive)                                     |
|----------------------------------------------------------------|
| "aggregate", "aggregates", "aggregate_query", "aggregatequery" |

---

## Chaining from

(Currently, no query chaining *from* `AggregateQuery` is defined.)

---

## Chaining to

(Currently, no query chaining *to* `AggregateQuery` is defined.)

---

## run() meta-parameters

`AggregateQuery()` accepts no extra meta-parameters when calling `run()`

---
