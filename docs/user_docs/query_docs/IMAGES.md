# Images
Images refer to the images that VMs can run on.
See [Openstack Docs](https://docs.openstack.org/api-ref/image/v2/index.html) for more info

**NOTE: `ImageQuery` will work with non-admin credentials.**
**However, for specific projects, or to query for images on all projects you need to have admin credentials
- set in `clouds.yaml`**

## Querying

To Query for Images using the Query Library, you can import `ImageQuery()` like so:

```python
from openstackquery import ImageQuery
```

`ImageQuery()` can then be used to setup and run queries - see [API.md](../API.md) for details on API calls

## Properties

An `Image` has the following properties:

| Return Type  | Property Name(s) (case-insensitive) | Description                                                         |
|--------------|-------------------------------------|---------------------------------------------------------------------|
| `string` (x) | "created_at"                        | The timestamp when this image was created.                          |
| `int`        | "progress"                          | Image creation percentage, 0 to 100. 100 once Image is created      |
| `string`     | "id", "uuid"                        | ID of the image                                                     |
| `string` (x) | "updated_at"                        | The timestamp when this image was last updated                      |
| `int`        | "min_ram", "ram"                    | The minimum disk size in GB that is required to boot the image.     |
| `int`        | "min_disk", "disk"                  | The minimum amount of RAM in MB that is required to boot the image. |
| `string`     | "name"                              | Name of the Image                                                   |
| `int`        | "size"                              | The size of the image data, in bytes.                               |
| `string`     | "status"                            | Image status                                                        |

(x) - These are UTC timestamps in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format
Any of these properties can be used for any of the API methods that takes a property - like `select`, `where`, `sort_by` etc

## Chaining
This section details valid mappings you can use to chain onto other queries or from other queries to chain into a `ImageQuery` object.
This applies to API calls `then` and `append_from` - see [API.md](../API.md) for details

## Query Alias
The aliases that can be used for the query when chaining are listed below:

| Aliases (case-insensitive)                     |
|------------------------------------------------|
| "image", "images", "image_query", "imagequery" |



## Chaining from
A `ImageQuery` can be chained to other queries.
The following shared-common properties are listed below (as well as the Query object they map to):

| Prop 1 | Prop 2     | Type        | Maps                          | Documentation            |
|--------|------------|-------------|-------------------------------|--------------------------|
| "id"   | "image_id" | One-to-Many | `ImageQuery` to `ServerQuery` | [SERVERS.md](SERVERS.md) |


## Chaining to
Chaining from other `ImageQuery` requires passing `image_query` or any of the aliases mentioned above as the `query_type`

| From          | Prop 1 | Prop 2     | Type        | Documentation            |
|---------------|--------|------------|-------------|--------------------------|
| `ServerQuery` | "id"   | "image_id" | Many-to-One | [SERVERS.md](SERVERS.md) |


## run() meta-parameters

`ImageQuery()` has the following meta-parameters that can be used when calling `run()` to fine-tune the query.

| Parameter Definition       | Optional?            | Description                                                                                                                                                                                                                                                               |
|----------------------------|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `from_projects: List[str]` | Yes                  | A list of project IDs or Names to limit search to<br/>Optional, if not given will run search in project given in clouds.yaml.<br/><br />Searching for specific projects in Openstack may not be possible without admin credentials - `as_admin` needs to be set to True ) |
| `all_projects: Bool`       | Yes, default = False | If True, will run query on all available projects available to the current user - set in clouds.yaml. <br/><br /> Searching for specific projects in Openstack not be possible without admin credentials - `as_admin` needs to be set to True )                           |
| `as_admin: Bool`           | Yes, default = False | If True, will run the query as an admin - this may be required to query outside of given project context set in clouds.yaml. <br/><br /> Make sure that the clouds.yaml context user has admin privileges                                                                 |


To query on all projects call `run()` like so:
```python
    ImageQuery.run(as_admin=True, all_projects=True)
```

To query on specific projects (you may not have access to) call `run()` like so (with admin creds):
```python
    ImageQuery.run(as_admin=True, from_projects=["name-or-id1", "name-or-id2"])
```
