from typing import List, Optional
from dataclasses import dataclass, fields

from handlers.client_side_handler import ClientSideHandler
from handlers.client_side_handler_generic import (
    ClientSideHandlerGeneric,
)
from handlers.client_side_handler_string import ClientSideHandlerString
from handlers.client_side_handler_datetime import (
    ClientSideHandlerDateTime,
)
from handlers.client_side_handler_integer import (
    ClientSideHandlerInteger,
)


@dataclass
class QueryClientSideHandlers:
    """
    Stores client side preset handlers
    """

    generic_handler: ClientSideHandlerGeneric
    string_handler: ClientSideHandlerString
    datetime_handler: Optional[ClientSideHandlerDateTime]
    integer_handler: Optional[ClientSideHandlerInteger]

    def to_list(self) -> List[ClientSideHandler]:
        values = []
        for field in fields(self):
            value = getattr(self, field.name)
            if value:
                values.append(value)
        return values
