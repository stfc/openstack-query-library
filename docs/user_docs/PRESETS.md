# Query Presets

Presets define how the query filters results when using the `where()` command

Presets define what query to run, they must be as atomic as possible - e.g. `EQUAL_TO`, `NOT_EQUAL_TO`, etc.
This allows the query to be defined by multiple presets and makes it clear what you want the query to find.

**Example:** To find all servers in a list of projects which are shutoff or errored - the queries can be:
```python
from openstackquery import ServerQuery

q1 = ServerQuery().where(preset="ANY_IN", prop="project_id", values=["project1", "project2"])
q2 = q1.where(preset="ANY_IN", prop="status", values=["ERROR", "SHUTOFF"])
```

# Reference

Query Library supports the following presets:

| Aliases (case insensitive)                                                                         | Description                                                                                            | Extra Parameters                                                              |
|----------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|
| `any_in`, `in`                                                                                     | Finds objects which have a property matching any of a given set of values                              | `values: List` - a list of property values to compare against                 |
| `not_any_in`, `not_in`                                                                             | Finds objects which have a property that does not match any of a given set of values                   | `values: List` - a list of property values to compare against                 |
| `equal_to`, `equal`, `==`                                                                          | Finds objects which have a property matching a given value                                             | `value` - a single value to compare against                                   |
| `not_equal_to` `not_equal`, `!=`                                                                   | Finds objects which have a property that does not match a given value                                  | `value` - a single value to compare against                                   |
| `matches_regex`, `regex`, `match_regex`, `re`                                                      | Finds objects which have a property that matches a regex pattern                                       | `value: str` - a string which can be converted into a regex pattern           |
| `greater_than`, `>`                                                                                | Finds objects which have an integer/float property greater than a threshold                            | `value: Union[int, float]` - an integer or float threshold to compare against |
| `less_than`, `<`                                                                                   | Finds objects which have an integer/float property less than a threshold                               | `value: Union[int, float]` - an integer or float threshold to compare against |
| `greater_than_or_equal_to`, `greater_or_equal` <br/>`more_than_or_equal_to`, `more_or_equal`, `>=` | Finds objects which have an integer/float property greater than or equal to a threshold                | `value: Union[int, float]` - an integer or float threshold to compare against |
| `less_than_or_equal_to`, `less_or_equal`, `<=`                                                     | Finds objects which have an integer/float property less than or equal to a threshold                   | `value: Union[int, float]` - an integer or float threshold to compare against |
| `older_than`, `older`, `>`                                                                         | Finds objects which have an datetime property older than a given relative time threshold               | * (see below)                                                                 |
| `younger_than`, `younger`, `newer_than`, `newer`, `<`                                              | Finds objects which have an datetime property younger than a given relative time threshold             | * (see below)                                                                 |
| `older_than_or_equal_to`, `older_or_equal`, `>=`                                                   | Finds objects which have an datetime property older than or equal to a given relative time threshold   | * (see below)                                                                 |
| `younger_than_or_equal_to`, `<=`                                                                   | Finds objects which have an datetime property younger than or equal to a given relative time threshold | * (see below)                                                                 |

### Extra Parameters
"*" -> Datetime Parameters
- `days: int` - (Optional) relative number of days since current time to compare against
- `hours: int` - (Optional) relative number of hours since current time to compare against
- `minutes: int` - (Optional) relative number of minutes since current time to compare against
- `seconds: int` - (Optional) relative number of seconds since current time to compare against

**NOTE:** At least one parameter from above must be given with a non-zero value for the preset to work, otherwise an error is produced
