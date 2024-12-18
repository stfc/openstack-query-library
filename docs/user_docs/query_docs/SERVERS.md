# Servers
Servers refer to Openstack Servers. A Server refers to a VM (Virtual Machine) that Openstack manages. Servers are
owned by a Project and a User.

See [Openstack Docs](https://docs.openstack.org/api-ref/identity/v3/index.html#servers-servers) for more info

**NOTE: `ServerQuery` will work with non-admin credentials.**
**However, for specific projects or to query all projects you may need to have admin credentials - set in `clouds.yaml`**

## Querying

To Query for Servers using the Query Library, you can import `ServerQuery()` like so:

```python
from openstackquery import ServerQuery
```

`ServerQuery()` can then be used to setup and run queries - see [API.md](../API.md) for details on API calls

## Properties

A `Server` has the following properties:

| Return Type  | Property Name(s) (case-insensitive) | Description                                                                                                                                                                                                                                          |
|--------------|-------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `string`     | `"flavor_id"`                       | The ID of the Flavor the Server is using                                                                                                                                                                                                             |
| `string`     | `"hypervisor_name"`                 | Name of the Hypervisor the Server is being hosted on                                                                                                                                                                                                 |
| `string`     | `"image_id"`                        | The ID of the Image the Server is using                                                                                                                                                                                                              |
| `string`     | `"project_id"`                      | The ID of the Project the Server is associated with                                                                                                                                                                                                  |
| `string` (x) | `"created_at"`                      | Timestamp of when the server was created.                                                                                                                                                                                                            |
| `string`     | `"description"`, `"desc"`           | User provided description of the server.                                                                                                                                                                                                             |
| `string`     | `"id"`, `"uuid"`                    | Unique ID Openstack has assigned the server.                                                                                                                                                                                                         |
| `string` (x) | `"updated_at"`                      | Timestamp of when this server was last updated.                                                                                                                                                                                                      |
| `string`     | `"vm_name"`, `"name"`               | User provided name for server                                                                                                                                                                                                                        |
| `string`     | `"vm_status"`, `"status"`           | The state this server is in. Valid values include <br/>ACTIVE, BUILDING, DELETED, ERROR, HARD_REBOOT, PASSWORD, PAUSED, <br/>REBOOT, REBUILD, RESCUED, RESIZED, REVERT_RESIZE, SHUTOFF, SOFT_DELETED, STOPPED, SUSPENDED, UNKNOWN, or VERIFY_RESIZE. |
| `string`     | `"user_id"`                         | The ID of the User that owns the server                                                                                                                                                                                                              |
| `string`     | `"ips"`, `"vm_ips"`, `"server_ips"` | Comma-separated list of IP addresses this server can be accessed through                                                                                                                                                                             |

(x) - These are UTC timestamps in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format
Any of these properties can be used for any of the API methods that takes a property - like `select`, `where`, `sort_by` etc

## Chaining
This section details valid mappings you can use to chain onto other queries or from other queries to chain into a `ProjectQuery` object.
This applies to API calls `then` and `append_from` - see [API.md](../API.md) for details

## Query Alias
The aliases that can be used for the query when chaining are listed below:

| Aliases (case-insensitive)                         |
|----------------------------------------------------|
| "server", "servers", "server_query", "serverquery" |


## Chaining from
A `ServerQuery` can be chained to other queries.
The following shared-common properties are listed below (as well as the Query object they map to):

| Prop 1              | Prop 2   | Type        | Maps                               | Documentation                    |
|---------------------|----------|-------------|------------------------------------|----------------------------------|
| `"user_id"`         | `"id"`   | Many-to-One | `ServerQuery` to `UserQuery`       | [USERS.md](USERS.md)             |
| `"project_id"`      | `"id"`   | Many-to-One | `ServerQuery` to `ProjectQuery`    | [PROJECTS.md](PROJECTS.md)       |
| `"flavor_id"`       | `"id"`   | Many-to-One | `ServerQuery` to `FlavorQuery`     | [FLAVORS.md](FLAVORS.md)         |
| `"image_id"`        | `"id"`   | Many-to-One | `ServerQuery` to `ImageQuery`      | [IMAGES.md](IMAGES.md)           |
| `"hypervisor_name"` | `"name"` | Many-to-One | `ServerQuery` to `HypervisorQuery` | [HYPERVISORS.md](HYPERVISORS.md) |



## Chaining to
Chaining from other `ServerQuery` requires passing `SERVER_QUERY` or any aliases mentioned above as the `query_type`

| From              | Prop 1 | Prop 2              | Type        | Documentation                    |
|-------------------|--------|---------------------|-------------|----------------------------------|
| `UserQuery`       | `id`   | `"user_id"`         | One-to-Many | [USERS.md](USERS.md)             |
| `ProjectQuery`    | `id`   | `"project_id"`      | One-to-Many | [PROJECTS.md](PROJECTS.md)       |
| `FlavorQuery`     | `id`   | `"flavor_id"`       | One-to-Many | [FLAVORS.md](FLAVORS.md)         |
| `ImageQuery`      | `id`   | `"image_id"`        | Many-to-One | [IMAGES.md](IMAGES.md)           |
| `HypervisorQuery` | `name` | `"hypervsior_name"` | One-to-Many | [HYPERVISORS.md](HYPERVISORS.md) |


## run() meta-parameters

`ServerQuery()` has the following meta-parameters that can be used when calling `run()` to fine-tune the query.

| Parameter Definition       | Optional?            | Description                                                                                                                                                                                                                                                               |
|----------------------------|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `from_projects: List[str]` | Yes                  | A list of project IDs or Names to limit search to<br/>Optional, if not given will run search in project given in clouds.yaml.<br/><br />Searching for specific projects in Openstack may not be possible without admin credentials - `as_admin` needs to be set to True ) |
| `all_projects: Bool`       | Yes, default = False | If True, will run query on all available projects available to the current user - set in clouds.yaml. <br/><br /> Searching for specific projects in Openstack may not be possible without admin credentials - `as_admin` needs to be set to True )                       |
| `as_admin: Bool`           | Yes, default = False | If True, will run the query as an admin - this may be required to query outside of given project context set in clouds.yaml. <br/><br /> Make sure that the clouds.yaml context user has admin privileges                                                                 |


To query on all projects remember to call `run()` like so:
```python
    ServerQuery.run(as_admin=True, all_projects=True)
```

To query on specific projects (you may not have access to) call `run()` like so (with admin creds):
```python
    ServerQuery.run(as_admin=True, from_projects=["name-or-id1", "name-or-id2"])
```
