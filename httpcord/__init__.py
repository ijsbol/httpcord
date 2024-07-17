from typing import Final

from .bot import HTTPBot
from .command import CommandResponse, Interaction


__all__: Final[tuple[str, ...]] = (
    "CommandResponse",
    "HTTPBot",
    "Interaction",
)

__version__: Final[str] = "0.0.02"
__author__: Final[str] = "Isabelle Phoebe <izzy@uwu.gal>"
