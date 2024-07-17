from typing import Final, TypedDict

from httpcord.enums import InteractionResponseType


__all__: Final[tuple[str, ...]] = (
    "JSONResponseError",
)


class JSONResponseError(TypedDict):
    error: str


class JsonResponseType(TypedDict):
    type: InteractionResponseType
