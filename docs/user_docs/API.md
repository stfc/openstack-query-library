
# Query Library API Reference
Query Library allows complex queries to be run on Openstack resources. It utilises an SQL-like syntax to setup
a query in a declarative way.

This document describes how to use the SQL-like API to run Openstack Queries

Remember to replace `query.run("openstack-domain", as_admin=True, all_projects=True)` by `query.run("openstack-domain")` if you don't have admin privileges in the OpenStack service. 

## Querying on Resources

The query library currently supports queries on the following Openstack resources

**NOTE**: In development - more query options will be added

| Openstack Resource                                                                                       | Description                            | Reference for Query Object               | How to Import                                |
|----------------------------------------------------------------------------------------------------------|----------------------------------------|------------------------------------------|----------------------------------------------|
| [Servers](https://docs.openstack.org/api-ref/compute/#servers-servers)                                   | Run a Query on Openstack Servers (VMs) | [SERVERS.md](query_docs/SERVERS.md)      | `from openstackquery import ServerQuery`     |
| [Users](https://docs.openstack.org/api-ref/identity/v3/index.html?expanded=list-users-detail#users)      | Run a Query on Openstack Users         | [USERS.md](query_docs/USERS.md)          | `from openstackquery import UserQuery`       |
| [Project](https://docs.openstack.org/api-ref/identity/v3/index.html?expanded=list-users-detail#projects) | Run a Query on Openstack Projects      | [PROJECTS.md](query_docs/PROJECTS.md)    | `from openstackquery import ProjectQuery`    |
| [Flavor](https://docs.openstack.org/api-ref/compute/#flavors)                                            | Run a Query on Openstack Flavors       | [FLAVORS.md](query_docs/FLAVORS.md)      | `from openstackquery import FlavorQuery`     |
| [Hypervisor](https://docs.openstack.org/api-ref/compute/#hypervisors-os-hypervisors)                     | Run a Query on Openstack Hypervisors   | [HYPERVISORS.md](query_docs/HYPERVISORS.md) | `from openstackquery import HypervisorQuery` |
| [Aggregate](https://docs.openstack.org/api-ref/compute/#host-aggregates-os-aggregates)                   | Run a Query on OpenStack Aggregates    | [AGGREGATES.md](query_docs/AGGREGATES.md) | `from openstackquery import AggregateQuery` |
| [Image](https://docs.openstack.org/api-ref/image/v2/index.html)                                          | Run a Query on OpenStack Images        | [IMAGES.md](query_docs/IMAGES.md) | `from openstackquery import ImageQuery` |

#
### select

`select()` allows you to run a query and output only specific properties from the results.
This is mutually exclusive to returning objects using `select_all()` which will return every available property


**Arguments**:

- `props`: one or more properties to collect (strings).
  - see the specific query page e.g. [SERVERS.md](query_docs/SERVERS.md) on supported properties and string aliases for that query

Running `select()` again will override all currently selected properties from previous `select()` call

`select()` and `select_all()` calls will be ignored when invoking `to_objects()`
`select()` is mutually exclusive to `select_all()`

**Examples**

```python
from openstackquery import ServerQuery
ServerQuery().select("server_name", "server_id")
```

#
### select\_all

`select_all()` will set the query to output all properties stored for the property to be returned .
Mutually exclusive to returning specific properties using select()

**Arguments**:
- None

Running `select_all()` will override currently selected properties from previous `select()` calls
`select_all()` will not work if `to_objects` is called - since it returns Openstack objects

#
### where
`where()` allows you to specify conditions for the query.

`where()` requires a preset-property pair to work.
- A preset is a special string that defines the logic to query by - see [PRESETS.md](PRESETS.md)
- A property is what the preset will be used on
- (optional) A set of key-word arguments that the preset-property pair require - like a value(s) to compare against

This can be called multiple times to define multiple conditions for the query - acts as Logical `AND`.

**Arguments**:

- `preset`: QueryPreset string to use
  - this specifies the logic to refine the query by. See [PRESETS.md](../PRESETS.md).
- `prop`: Property string alias that the query preset will be used on -
  - some presets can only accept certain properties - see [FILTER_MAPPINGS.md](../FILTER_MAPPINGS.md)
- `kwargs`: a set of optional arguments to pass along with the query preset
  - these kwargs are dependent on the preset - see [PRESETS.md](../PRESETS.md)

**Example(s)**

To query for servers which are in "error" state - the values would be:
- preset - `"equal_to"`
- prop - `"status"`
- value(s) - `value="ERROR"`

the `where` call would be like so:
```python
from openstackquery import ServerQuery

# create a ServerQuery
query = ServerQuery()
query.select_all()

# setup filter status = ERROR
query.where(
    preset="equal_to",
    prop="status",
    value="ERROR"
)
```

#
### sort\_by

`sort_by` allows you to sort results by given property(ies) before outputting.
It allows sorting by multiple keys if you provide multiple `sort_by` tuples.

**Arguments**:

- `sort_by`: Takes any number of tuples - the tuples must consist of two values:
  - a property (string) to sort by
  - a string representing the sort order
    - `"ascending"` for ascending
    - `"descending"` for descending

| SortOrder String         | Description              |
|--------------------------|--------------------------|
| `"ascending"`, `"asc"`   | sort in ascending order  |
| `"descending"`, `"desc"` | sort in descending order |

**Note**: You can sort by properties you haven't 'selected' for using `select()`

**Examples**

```python
from openstackquery import ServerQuery

# create a ServerQuery
query = ServerQuery()
query.select("id", "name")

# run the query
query.run("openstack-domain", as_admin=True, all_projects=True)

# sort by name in descending, then sort by id in ascending
query.sort_by(
  ("id", "descending"),
  ("name", "ascending")
)

# or using equivalent string aliases
query.sort_by(
  ("server_id", "descending"),
  ("server_name", "ascending")
)

print(query.to_string())
```

results sorted by server name in descending (alphabetical) order, then if server name is the same,
we sort by server_id in ascending order etc.
```commandline
+--------------------------------------------+--------------------------------------+
| server_name                                | server_id                            |
+==================================================================================+
| foo2                                       | 3                                    |
+--------------------------------------------+--------------------------------------+
| foo                                        | 1                                    |
+--------------------------------------------+--------------------------------------+
| foo                                        | 2                                    |
+--------------------------------------------+--------------------------------------+
| bar                                        | 4                                    |
+--------------------------------------------+--------------------------------------+
```

#
### group\_by

`group_by` allows you to group the results before outputting by either:
- unique values found for a property specified in `group_by`
- a set of pre-defined groups which define how to group results based on their value of the property specified in `group_by`


Public method used to configure how to group results.

**Arguments**:

- `group_by`: a property (string) representing the property you want to group by
- `group_ranges`: (optional) a dictionary of group mappings
  - the keys are unique group names
  - the values are a list of values that `group_by` property could have to be included in that group
- `include_ungrouped_results`: (optional) flag that if true - will include an "ungrouped" group (Default is `False`)
  - ungrouped group will contain all results that have a `group_by` property value that does not match any of the
  groups set in `group_ranges`

**Note**: You can group by properties you haven't 'selected' for using `select()`

**Examples**
Running an `ANY_IN` command and grouping results

```python

from openstackquery import ServerQuery

# create a ServerQuery
query = ServerQuery()
query.select("id", "name")

# setup filter server_status = ERROR
query.where(
    preset="ANY_IN",
    prop="server_status",
    values=["ERROR", "SHUTOFF"]
)
query.run("openstack-domain", as_admin=True, all_projects=True)
query.group_by("server_status")

# holds a dictionary - where keys are unique values of "server_status" in results
# in this case - ERROR and SHUTOFF since we queried for them
x = query.to_objects()
```

```commandline
> {"ERROR": [
        {"server_id": 1, "server_name": "foo"},
        {"server_id": 2, "server_name": "bar"},
   ],
   "SHUTOFF": [
        {"server_id": 3, "server_name": "biz"},
        {"server_id": 4, "server_name": "baz"},
   ]
```

#
### run

`run()` will run the query. `run()` will apply all predefined conditioned set by `where` calls


**Arguments**:

- `cloud_account`: A string representing the clouds configuration to use
  - this should be the domain set in the `clouds.yaml` file located in `.config/openstack/clouds.yaml` (or `/etc/openstack/clouds.yaml`)

- `from_subset`: (optional) a subset of openstack resources to run query on instead of querying for them using openstacksdk
  - **NOTE:** this is going to be deprecated soon - look at using `then()` or `append_from()` for a better way to
  chain the result of one query onto another

- `kwargs`: keyword args that can be used to configure details of how query is run
  - see specific documentation for resource for valid keyword args you can pass to `run()`

#
### to\_objects

`to_objects` is an output method that will return results as openstack objects.

Like all output methods - it will parse the results set in `sort_by()`, `group_by()` and requires `run()` to have been called first
- this method will not run `select` - instead outputting raw results (openstack resource objects)

This is either returned as a list if `group_by` has not been set, or as a dict if `group_by` was set

**Arguments**:

- `groups`: a list of group keys to limit output by - this will only work if `group_by()` has been set - else it produces an error

**Examples**

```python

from openstackquery import ServerQuery

# create a ServerQuery
query = ServerQuery()
query.select("server_id", "server_name")

# setup filter server_status = ERROR
query.where(
    preset="EQUAL_TO",
    prop="server_status",
    value="ERROR"
)
query.run("openstack-domain", as_admin=True, all_projects=True)
x = query.to_objects()
```

`x` holds the following: A list of openstack Server objects
```commandline
> [openstack.compute.v2.server.Server(...), openstack.compute.v2.server.Server(...), ...]
```

#
### to\_props
`to_props` is an output method that will return results as a dictionary of selected properties.

Like all output methods - it will parse the results set in `sort_by()`, `group_by()` and requires `run()` to have been called first
- This method will parse results to get properties that we 'selected' for - from a `select()` or a `select_all()` call
- If this query is chained from previous query(ies) by `then()` - the previous results will also be included
- If any `append_from` calls have been run - the properties appended will also be included

This is either returned as a list if `group_by` has not been set, or as a dict if `group_by` was set

**Arguments**:

- `flatten`: (optional) boolean flag which will flatten results if true (default is `False`)

If True will flatten the results by selected for properties:

Instead of returning:
```python
print(query.to_props(flatten=False))

[

  # first result
  { "project_name": "foo", "project_id": "bar" },

  # second result
  { "project_name": "foo1", "project_id": "bar1" },
  ...
]
```

it will return:
```python
print(query.to_props(flatten=True))

{
    "project_name": ["foo", "foo1"],
    "project_id": ["bar", "bar1"]
}
```

If the results are grouped:

Instead of returning:
```python
print(grouped_query.to_props(flatten=False))

{
    "group1": [
        { "project_name": "foo", "project_id": "bar" },
        { "project_name": "foo1", "project_id": "bar1" },
    ],
    "group2": [
        {"project_name": "biz", "project_id": "baz"},
        {"project_name": "biz1", "project_id": "baz1"}
    ]
}
```
It will return:
```python
print(grouped_query.to_props(flatten=True))

{
    "group1": {
        "project_name": ["foo", "foo1"],
        "project_id": ["bar", "bar1"]
    },
    "group2": {
        "project_name": ["biz", "biz1"],
        "project_id": ["baz", "baz1"]
    }
}
```

- `groups`: (optional) a list of group keys to limit output by - this will only work if `group_by()` has been set - else it produces an error

**Examples**

```python

from openstackquery import ServerQuery

# create a ServerQuery
query = ServerQuery()
query.select("id", "name")
query.run("openstack-domain", as_admin=True, all_projects=True)
# setup filter server_status = ERROR
query.where(
    preset="equal_to",
    prop="status",
    value="ERROR"
)

x = query.to_props()
# x would hold a list of dictionaries that contain only the info you've selected
```
```commandline
> [{"server_id": 1, "server_name": "foo"}, {"server_id": 2, "server_name": "bar"}, ...]
```

if `flatten=True`
```python
  x = query.to_props(flatten=True)
  # x would hold a list of dictionaries that contain only the info you've selected
```
```commandline
> {"server_name": ["foo", "bar", ...], "server_id": [1, 2, ...]}
```

#
### to\_string
`to_string` is an output method that will return results as a tabulate table(s) (in string format).

Like all output methods - it will parse the results set in `sort_by()`, `group_by()` and requires `run()` to have been called first
- This method will parse results to get properties that we 'selected' for - from a `select()` or a `select_all()` call
- If this query is chained from previous query(ies) by `then()` - the previous results will also be included
- If any `append_from` calls have been run - the properties appended will also be included

**Arguments**:

- `title`: An optional title to print on top
- `groups`: a list of group keys to limit output by - this will only work if `group_by()` has been set - else it produces an error
- `include_group_titles`: A boolean (Default True), if True, will print the group key as a subtitle before printing each selected group table, if False no subtitle will be printed.
- `kwargs`: kwargs to pass to tabulate to tweak table generation
  - see [tabulate](https://pypi.org/project/tabulate/) for valid kwargs
  - note `to_string` calls tabulate with `tablefmt="plaintext"`

**Examples**

```python

from openstackquery import ServerQuery

# create a ServerQuery
query = ServerQuery()
query.select("id", "name")

# setup filter server_status = ERROR
query.where(
    preset="equal_to",
    prop="status",
    value="ERROR"
)
query.run("openstack-domain", as_admin=True, all_projects=True)

print(query.to_string())

```
```commandline
+--------------------------------------------+--------------------------------------+
| server_name                                | server_id                            |
+==================================================================================+
| foo                                        | 1                                    |
+--------------------------------------------+--------------------------------------+
| bar                                        | 2                                    |
+--------------------------------------------+--------------------------------------+
```

#
### to\_html
`to_html` is an output method that will return results as a tabulate table(s) (in string format - in html format).

Like all output methods - it will parse the results set in `sort_by()`, `group_by()` and requires `run()` to have been called first
- This method will parse results to get properties that we 'selected' for - from a `select()` or a `select_all()` call
- If this query is chained from previous query(ies) by `then()` - the previous results will also be included
- If any `append_from` calls have been run - the properties appended will also be included


**Arguments**:

- `title`: An optional title to print on top
- `groups`: a list of group keys to limit output by - this will only work if `group_by()` has been set - else it produces an error
- `include_group_titles`: A boolean (Default True), if True, will print the group key as a subtitle before printing each selected group table, if False no subtitle will be printed.
- `kwargs`: kwargs to pass to tabulate to tweak table generation
  - see [tabulate](https://pypi.org/project/tabulate/) for valid kwargs
  - note `to_html` calls tabulate with `tablefmt="html"`


**Examples**

```python

from openstackquery import ServerQuery

# create a ServerQuery
query = ServerQuery()
query.select("id", "name")

# setup filter server_status = ERROR
query.where(
    preset="equal_to",
    prop="status",
    value="ERROR"
)
query.run("openstack-domain", as_admin=True, all_projects=True)

print(query.to_html())

```
```commandline
<table>
<thead>
<tr><th>server_id                     </th><th>server_name                               </th></tr>
</thead>
<tbody>
<tr><td>1                             </td><td>foo                                       </td></tr>
<tr><td>2                             </td><td>bar                                       </td></tr>

```

#
### to_csv
`to_csv` is an output method that will return the results as a csv string. If the results are grouped, different strings will be returned for each.

Grouped data can be flattened by setting `flatten_groups=True`. Grouped data will then be merged into a single csv, with a `group` column.

Like all output methods - it will parse the results set in `sort_by()`, `group_by()` and requires `run()` to have been called first
- This method will parse results to get properties that we 'selected' for - from a `select()` or a `select_all()` call
- If this query is chained from previous query(ies) by `then()` - the previous results will also be included
- If any `append_from` calls have been run - the properties appended will also be included

**Arguments**:

- `groups`: *(optional)* a list of group keys to limit output by - this will only work if `group_by()` has been set - else it produces an error
- `flatten_groups`: *(optional, default=False)* if True, grouped data is merged into a single csv string with a `group` column.

**Examples**:
Without grouping:
```python
from openstackquery import ServerQuery

query = ServerQuery()
query.select("id", "name", "status")
query.where(preset="equal_to", prop="status", value="ERROR")
query.run("openstack-domain", as_admin=True, all_projects=True)

csv_output = query.to_csv()
print(csv_output)
```

```commandline
id,name,status
1,foo,ERROR
2,bar,ERROR
3,baz,ACTIVE
4,bif,ACTIVE
```

With grouping:
```python
query.group_by("status")
csv_output = query.to_csv()
print(csv_output)
```

```commandline
# Group: ERROR
id,name,status
1,foo,ERROR
2,bar,ERROR

# Group: ACTIVE
id,name,status
3,baz,ACTIVE
4,bif,ACTIVE
```

With grouping and flattening:
```python
query.group_by("status")
csv_output = query.to_csv(flatten_groups=True)
print(csv_output)
```

```commandline
id,name,status,group
1,foo,ERROR,ERROR
2,bar,ERROR,ERROR
3,baz,ACTIVE,ACTIVE
4,bif,ACTIVE,ACTIVE
```

### to_json

`to_json` is an output method that will return results as a JSON-formatted string.

Like all output methods, it will parse the result set built using `sort_by()`, `group_by()`, and requires `run()` to have been called first.

- This method will parse results to get properties that were selected via `select()` or `select_all()`
- If this query is chained from previous query(ies) using `then()`, the previous results will also be included
- If any `append_from()` calls have been made, the appended properties will also be included

**Arguments**:

- `groups`: *(optional)* A list of group keys to limit output by – only works if `group_by()` has been used. Otherwise, this will raise an error.
- `flatten_groups`: *(optional, default=False)*  
  - If `False` and the results are grouped, the output will be a JSON object (dict) where each key is a group name and the value is a list of results for that group.
  - If `True` and the results are grouped, all grouped results are flattened into a single list, and each entry includes a `"group"` field indicating which group it originally belonged to.
- `pretty`: *(optional, default=False)* If True, returns a pretty-printed JSON string with indentation for readability.

**Examples**

Without grouping:
```python
from openstackquery import ServerQuery

query = ServerQuery()
query.select("id", "name", "status")
query.where(preset="equal_to", prop="status", value="ERROR")
query.run("openstack-domain", as_admin=True, all_projects=True)

json_output = query.to_json()
print(json_output)
```

```json
[{"id": 1, "name": "foo", "status": "ERROR"}, {"id": 2, "name": "bar", "status": "ERROR"}]
```

With `pretty=True`:
```python
json_output = query.to_json(pretty=True)
print(json_output)
```

```json
[
    {
        "id": 1,
        "name": "foo",
        "status": "ERROR"
    },
    {
        "id": 2,
        "name": "bar",
        "status": "ERROR"
    }
]
```

With grouping:
```python
query.group_by("status")
json_output = query.to_json(pretty=True)
print(json_output)
```

```json
{
    "ERROR": [
        {"id": 1, "name": "foo", "status": "ERROR"},
        {"id": 2, "name": "bar", "status": "ERROR"}
    ],
    "ACTIVE": [
        {"id": 3, "name": "baz", "status": "ACTIVE"},
        {"id": 4, "name": "bif", "status": "ACTIVE"}
    ]
}
```

With grouping and flattening:
```python
json_output = query.to_json(flatten_groups=True, pretty=True)
print(json_output)
```

```json
[
    {"id": 1, "name": "foo", "status": "ERROR", "group": "ERROR"},
    {"id": 2, "name": "bar", "status": "ERROR", "group": "ERROR"},
    {"id": 3, "name": "baz", "status": "ACTIVE", "group": "ACTIVE"},
    {"id": 4, "name": "bif", "status": "ACTIVE", "group": "ACTIVE"}
]
```

#
### then
`then()` chains current query onto another query of a different type.
It takes the results of the current query and uses them to run another query

This can only work if the current query and the next query have a shared common property

- Query must be run first by calling `run()` before calling `then()`
- A shared common property must exist between this query and the new query
   - i.e. both ServerQuery and UserQuery share the 'USER_ID' property so chaining is possible between them


**NOTE:** Any parsing calls - i.e. `group_by` or `sort_by` will be ignored

**NOTE:** You will NOT be able to group/sort by forwarded properties in the new query

**Arguments**:

- `query_type`: a string representing the new query to chain into
  - see specific documentation for `query_types` under `docs/user_docs/query_docs`

- `keep_previous_results`: flag that:
  - If True - will forward outputs from this query (and previous chained queries) onto new query.
  - If False - runs the query based on the previous results as a filter without adding additional fields

**Examples:**
See [USAGE.md](USAGE.md) for complex query examples where you would use `then()`

#
### append\_from
`append_from()` appends specific properties from other queries to the output.

This method will run a secondary query on top of this one to get required properties and append each result to the results of this query

- Query must be run first by calling `run()` before calling `append_from()`
- A shared common property must exist between this query and the new query
   - i.e. both ServerQuery and UserQuery share the `'USER_ID'` property so `append_from` is possible between them
   - see specific documentation for resource for valid ways to chain

**NOTE:** You will NOT be able to group/sort by forwarded properties in the new query


**Arguments**:

- `query_type`: a string representing the new query to chain into
  - see specific documentation for resource for valid ways `query_types`

- `cloud_account`: A string for the clouds configuration to use
  - this should be the domain set in the `clouds.yaml` file located in `.config/openstack/clouds.yaml` (or `/etc/openstack/clouds.yaml`)
- `props`: a list of strings representing the properties to collect from new query.
  - see specific documentation for resource you want to append props `docs/user_docs/query_docs`


**Examples:**
See [USAGE.md](USAGE.md) for complex query examples where you would use `append_from()`
