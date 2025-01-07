# Usage
The following document contains different ways to use the query library.

The examples assume:
* you do not have admin privileges for the OpenStack service
* the name of your Cloud domain is `prod`

You can find the actual Cloud domain name in your `clouds.yaml` file.

If you have admin privileges, the queries can be performed for all projects in OpenStack. For that, just replace the lines

```python
query.run("prod")
```

by

```python
query.run("prod", as_admin=True, all_projects=True)
```

## Simple Query
Find Errored and Shutoff VMs

```python
from openstackquery import ServerQuery

# Create a Query Object that will search for Openstack VMs
query = ServerQuery()

# Select - when outputting - only output the selected properties from each VM
query.select("name", "id")

# Where - define a preset ("any in" = match any value given), a property to apply it to (server status) and value/s to look for (ERROR, SHUTOFF)
query.where("any_in", "status", values=["ERROR", "SHUTOFF"])

# Run - this will run the query in the "prod" cloud domain and will find VMs in your project set in `clouds.yaml`.
query.run("prod")

# Group By - This will group the results by a property - project_id
# NOTE: group by property and selected property are completely independent
query.group_by("project_id")

# Output the query results to table(s) (stored as a string)
print(query.to_string())
```


## Using more than one where()

Find Errored and Shutoff VMs
- AND haven't been updated in 60 days

```python
from openstackquery import ServerQuery


query = ServerQuery()
query.select("name", "id")
query.where("any_in", "status", values=["ERROR", "SHUTOFF"])

# ADDITIONAL WHERE - ACTS AS LOGICAL AND
# Extra query preset refines search to look for errored and shutoff VMs that haven't been updated in 60 days
query.where("older_than", "last_updated_date", days=60)


query.run("prod")
query.group_by("id")
print(query.to_string())
```

## Chaining with then()

Find Errored and Shutoff VMs
- AND haven't been updated in 60 days
- AND the user who made the VM must belong to a specific user domain


```python
from openstackquery import UserQuery

# setup and run a User Query to get user info for all users in a specific domain
user_query = UserQuery()
user_query.select("name", "email")
user_query.where("equal_to", "domain_id", value="stfc")
user_query.run("prod")

# We're going to create a Server Query using the results from the first query

# This is the same as doing:
# user_ids = user_query.group_by("id").to_props().keys()
# ServerQuery().where("any_in", "user_id", values=list(user_ids))

# NOTE: setting keep_previous_results=True will carry over properties we've selected for from the previous query
server_query = user_query.then("SERVER_QUERY", keep_previous_results=True)

# Then we continue as normal!
server_query.select("name", "id")
server_query.where("any_in", "status", values=["ERROR", "SHUTOFF"])
server_query.where("older_than", "last_updated_date", days=60)
server_query.run("prod")
server_query.group_by("project_id")

# These results will contain VM associated values for user_name and user_email
# results will only contain VMs belonging to users in "stfc"
print(server_query.to_string())
```

## Selecting external props using append_from()

Find Errored and Shutoff VMs
- AND haven't been updated in 60 days
- AND the user who made the VM must belong to a specific user domain.
- AND include the PROJECT_NAME

```python
from openstackquery import UserQuery

# setup and run a User Query to get user info for all users in a specific domain
user_query = UserQuery()
user_query.select("name", "email")
user_query.where("equal_to", "domain_id", value="stfc")
user_query.run("prod")

server_query = user_query.then("SERVER_QUERY", keep_previous_results=True)
server_query.select("name", "id")
server_query.where("any_in", "status", values=["ERROR", "SHUTOFF"])
server_query.where("older_than", "last_updated_date", days=60)
server_query.run("prod")

# We need to get project name by running append_from()
# append_from() command below is the same as doing the following:
#   project_ids = server_query.group_by("project_id").to_props().keys()
#   p = ProjectQuery().select("name").where(
#        "any_in", "id", values=list(project_ids)
#   )
#   p.run("prod")
#   res = p.to_props()
# `res` is then combined zipped together into the current output
server_query.append_from("PROJECT_QUERY", "prod", ["project_id"])

# Note it's not possible to group by external properties (yet)
server_query.group_by("project_id")

# This will print out results and includes project name for every VM too
server_query.to_string()
```

# Grouping Usage

## Group By Unique Values
By default - the unique values of a given property found in results as the 'group_key'
```python
from openstackquery import ServerQuery

query = ServerQuery().select("id", "name")
query.where("any_in", "status", values=["ERROR", "SHUTOFF"])
query.run("prod")

# groups by unique values of server_status found in results
#   - in this case we'll get 2 groups - 'ERROR' and 'SHUTOFF' are the group keys
query.group_by("status")
```

## Group By Given Group Keys
You can specify you're own group_keys by setting the values that belong to each group like so:
```python
from openstackquery import ServerQuery

query = ServerQuery().select("id", "name")
query.where("any_in", "status", values=["ERROR", "SHUTOFF"])
query.run("prod")

# groups by pre-configured groups
group_keys = {
    # first group must have VMs belonging to project-id1 and project-id2
    "group1": ["project-id1", "project-id2"],
    # second group must have VMs belonging to project-id3 and project-id3
    "group2": ["project-id3", "project-id4"]
}
# groups by pre-configured group keys
#   - in this case we'll get 2 groups - group1 and group2
#   - group1 will contain VMs belonging to project with ids project-id1 and project-id2
#   - group2 will contain VMs belonging to project with ids project-id3 and project-id4
#   - all other VMs will be ignored
query.group_by("project_id", group_keys=group_keys)
```

### Note About Aliases

The strings used for presets, properties, and query types

1. For Preset aliases for use with `where()` see [Presets.md](PRESETS.md)
2. For Property aliases for use with `select()`, `where()` and others, see the specific page in [query_docs](query_docs)
3. For Query aliases for use with `then()`, append_from()`, see the specific page in [query_docs](query_docs)
4. For other aliases, see API method reference in [API.md](API.md)
