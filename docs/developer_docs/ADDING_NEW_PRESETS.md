# Adding A New Preset

## **1. Add the preset name to the QueryPresets enum class in `openstackquery/enums/query_presets.py`**

e.g.
```python
class QueryPresets(EnumWithAliases):
    """
    Enum class which holds generic query comparison operators
    """

    EQUAL_TO = auto()
    ...
    NEW_PRESET = auto() # <- we add this line to represent a new preset enum belonging to the 'Generic' group
```

(Optional) Add alias mappings for the preset - see [Adding Aliases](ADDING_ALIASES.md)

## **2. Create a function to act as the client-side filter function for your new query preset

Client-side filter functions are located in `openstackquery/handlers/client_side_filters.py`

The filter function must:
- **take as input at least one parameter - `prop`**:
  - `prop` (must be the first positional argument) - represents the property value the filter acts on.
  - Can also take other parameters are extra arguments that are required for the preset to work
- **return a boolean**
   - `True` if the prop passes filter
   - `False` if not

```python
def prop_new_preset_filter_func(self, prop: Any, arg1, arg2):
    """
    A new preset filter - takes a property value, performs some logic and returns a boolean if
    property passes a filter or not
    :param prop: property value to check
    :param arg1: some arg the filter uses
    :param arg2: some other arg the filter uses
    :returns: True or False
    """
    # Define your filter logic here
```

## **3. Edit the corresponding handler class in `openstackquery/handlers/client_side_handler.py`.**

Here you must:
- add a 'client-side' filter function as a method
- add the mapping between the enum and filter function in self._filter_functions.

e.g. editing `client_side_handler_generic.py`
```python
from openstackquery.handlers.client_side_filters import (
    prop_new_preset_filter_func # newly made filter func
)

class ClientSideHandler(HandlerBase):
...

def __init__(self, preset_prop_mappings: ClientSidePresetPropertyMappings):
    self._filter_functions = {
        QueryPresets.EQUAL_TO: self._prop_equal_to,
        ...
        QueryPresets.NEW_PRESET: prop_new_preset_filter_func # <- 2) add the enum-to-function mapping
    }
...
```

## **3. Edit the query class mappings for each Query class you wish to use the preset in**
Each Query Class has a set of mappings which configures certain aspects of the Query (See [FILTER_MAPPINGS.md](FILTER_MAPPINGS.md) for details).

One of these aspects is which preset-property pair can be used together when calling `where()` on the class.

Here you must:
1. Evaluate which Query class should be able to use your new preset
2. For each Query class you've chosen, evaluate which property(ies) the preset should work on
3. Add chosen mappings to `get_client_side_handlers` method in the Mappings class for each chosen Query
   - these are located in `openstackquery/mappings/<query-resource>_mapping.py`

e.g. Adding Mappings for `QueryPresetsGeneric.NEW_PRESET` to `ServerQuery`. Editing `openstackquery/mappings/server_mapping.py`
```python

class ServerMapping(MappingInterface):
    ...

    @staticmethod
    def get_client_side_handler() -> ClientSideHandler:
        ...
        return ClientSideHandler(

            {
                # Line below maps EQUAL_TO preset on all available properties
                # ["*"] - represents all props
                QueryPresets.EQUAL_TO: ["*"],
                # ...
                # Line below maps our 'new preset' to two properties which the preset can run on
                # Running the preset on any other property leads to an error
                QueryPresets.NEW_PRESET: [
                    ServerProperties.SERVER_ID,
                    ServerProperties.SERVER_NAME
                ]
            }
        )
    ...
```

## **4. (Optional) Add server-side filters for the preset**

To add a server-side filter you must:
1. Read the Openstack API documentation for each Query the preset works on
    - links to the specific docs can be found in the docstring of `get_server_side_handler` method for the query
      - located in `mappings/<query-resource>_mapping.py`

2. Once a server-side filter is discovered for your new preset add a mapping to `get_server_side_handler` method
e.g. Adding server-side mapping for `QueryPresetsGeneric.NEW_PRESET` to `ServerQuery`. Editing `mappings/server_mapping.py`
```python

class ServerMapping(MappingInterface):
    #...

    @staticmethod
    def get_server_side_handler() -> ServerSideHandler:
        #...
        return ServerSideHandler(
            {
                #...
                QueryPresets.NEW_PRESET: {
                    # adding a server-side mapping for NEW_PRESET when given SERVER_ID
                    ServerProperties.SERVER_ID: lambda value, arg1, arg2:
                        {"server-side-kwarg": value, "server-side-arg1": arg1, "server-side-arg2": arg2}
                }
            }
    )
    #...
```
