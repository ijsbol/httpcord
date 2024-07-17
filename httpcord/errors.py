from typing import Final


__all__: Final[tuple[str, ...]] = (
    "HTTPCordException",
    "UnknownCommand",
)


class HTTPCordException(Exception):
    pass

class UnknownCommand(HTTPCordException):
    pass
