from abc import ABC, abstractmethod
from enums.query_presets import QueryPresets
from enums.props.prop_enum import PropEnum


class HandlerBase(ABC):
    """
    Abstract Base class for handlers.
    This class is an abstract class for a generic handler
    A handler stores a mapping between a preset and a function.
    """

    @abstractmethod
    def check_supported(self, preset: QueryPresets, prop: PropEnum) -> bool:
        """
        Method used to return if a preset and prop are supported by the handler
        :param preset: An Enum which represents a preset
        :param prop: An Enum which represents a property for preset to act on
        """

    @abstractmethod
    def preset_known(self, preset: QueryPresets) -> bool:
        """
        Method used to return if a preset is supported by the handler
        :param preset: An Enum which represents a preset
        """
