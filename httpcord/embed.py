from typing import Any, Final


__all__: Final[tuple[str, ...]] = (
    "Embed",
)


class EmbedFooter:
    __slots__: Final[tuple[str, ...]] = (
        "text",
        "icon_url",
    )

    def __init__(
        self,
        *,
        text: str,
        icon_url: str | None = None,
    ) -> None:
        self.text = text
        self.icon_url = icon_url

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "icon_url": self.icon_url,
        }


class EmbedField:
    __slots__: Final[tuple[str, ...]] = (
        "name",
        "value",
        "inline",
    )

    def __init__(
        self,
        *,
        name: str | None = None,
        value: str | None = None,
        inline: bool = False,
    ) -> None:
        self.name = name
        self.value = value
        self.inline = inline

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "inline": self.inline,
        }


class Embed:
    __slots__: Final[tuple[str, ...]] = (
        "title",
        "description",
        "colour",
        "_fields",
        "_footer",
    )

    def __init__(
        self,
        *,
        title: str | None = None,
        description: str | None = None,
        colour: int | None = None,
    ) -> None:
        self.title = title
        self.description = description
        self.colour = colour
        self._fields: list[EmbedField] = []
        self._footer: EmbedFooter | None = None

    def add_field(
        self,
        *,
        name: str | None = None,
        value: str | None = None,
        inline: bool = False,
    ) -> None:
        self._fields.append(EmbedField(
            name=name,
            value=value,
            inline=inline,
        ))

    def set_footer(
        self,
        text: str,
        *,
        icon_url: str | None = None,
    ) -> None:
        self._footer = EmbedFooter(
            text=text,
            icon_url=icon_url,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "description": self.description,
            "color": self.colour,
            "footer": (
                {} if not self._footer
                else self._footer.to_dict()
            ),
            "fields": [f.to_dict() for f in self._fields],
        }
