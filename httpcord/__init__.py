from typing import Final

from .bot import HTTPBot
from .command import CommandResponse, Interaction


__all__: Final[tuple[str, ...]] = (
    "CommandResponse",
    "HTTPBot",
    "Interaction",
)

__version__: Final[str] = "a0.0.1"
