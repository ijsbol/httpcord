"""
MIT License

Copyright (c) 20234 Isabelle Phoebe <izzy@uwu.gal>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from enum import StrEnum
from typing import Literal


__all__: tuple[str, ...] = (
    "SupportedLocales",
    "DEFAULT_LOCALE",
    "LocaleDict",
    "Locale",
)

SupportedLocalesLiterals = Literal[
    "id", "da", "de", "en-GB", "en-US", "es-ES",
    "es-419", "fr", "hr", "it", "lt", "hu", "nl",
    "no", "pl", "pt_BR", "ro", "fi", "sv_SE", "vi",
    "tr", "cs", "el", "bg", "ru", "uk", "hi", "th",
    "zh_CN", "ja", "zh_TW", "ko",
]


class SupportedLocales(StrEnum):
    id = "id"  # Indonesian
    da = "da"  # Danish
    de = "de"  # German
    en_GB = "en_GB"  # English (UK)
    en_US = "en_US"  # English (US)
    es_ES = "es_ES"  # Spanish (Spain)
    es_419 = "es_419"  # Spanish (Latin America)
    fr = "fr"  # French
    hr = "hr"  # Croatian
    it = "it"  # Italian
    lt = "lt"  # Lithuanian
    hu = "hu"  # Hungarian
    nl = "nl"  # Dutch
    no = "no"  # Norwegian
    pl = "pl"  # Polish
    pt_BR = "pt_BR"  # Portuguese (Brazil)
    ro = "ro"  # Romanian
    fi = "fi"  # Finnish
    sv_SE = "sv_SE"  # Swedish
    vi = "vi"  # Vietnamese
    tr = "tr"  # Turkish
    cs = "cs"  # Czech
    el = "el"  # Greek
    bg = "bg"  # Bulgarian
    ru = "ru"  # Russian
    uk = "uk"  # Ukrainian
    hi = "hi"  # Hindi
    th = "th"  # Thai
    zh_CN = "zh_CN"  # Chinese (China)
    ja = "ja"  # Japanese
    zh_TW = "zh_TW"  # Chinese (Taiwan)
    ko = "ko"  # Korean

    def __str__(self) -> str:
        return self.value.replace("_", "-")


DEFAULT_LOCALE = "en-US"
LocaleDict = dict[SupportedLocalesLiterals, str]


class Locale:
    __slots__: tuple[str, ...] = (
        "name_localisations",
        "description_localisations",
    )

    def __init__(
        self,
        name: str | None = None,
        description: str | None = None,
        *,
        name_localisations: LocaleDict | None = None,
        description_localisations: LocaleDict | None = None,
    ) -> None:
        import enum  # Import for validation
        self.name_localisations: LocaleDict = {}
        self.description_localisations: {}
        if name_localisations:
            for key in name_localisations:
                if not any(key == locale.value for locale in SupportedLocales):  # Validate against SupportedLocales
                    raise ValueError(f'Invalid locale key: {key}')
            self.name_localisations = name_localisations
        if description_localisations:
            for key in description_localisations:
                if not any(key == locale.value for locale in SupportedLocales):  # Validate against SupportedLocales
                    raise ValueError(f'Invalid locale key: {key}')
            self.description_localisations = description_localisations
        if name:
            self.name_localisations[DEFAULT_LOCALE] = name  # Assuming DEFAULT_LOCALE is valid
        if description:
            self.description_localisations[DEFAULT_LOCALE] = description  # Assuming DEFAULT_LOCALE is valid

    def get_default(
        self,
        key: Literal[
            "name_localisations",
            "description_localisations",
        ],
    ) -> str:
        if key == "name_localisations":
            value = self.name_localisations.get(DEFAULT_LOCALE)
            if value is None:
                return list(self.name_localisations.values())[0]
            return value
        elif key == "description_localisations":
            value = self.description_localisations.get(DEFAULT_LOCALE)
            if value is None:
                return list(self.description_localisations.values())[0]
            return value
        else:
            raise KeyError(key)

    def __getitem__(
        self,
        key: Literal[
            "name_localisations",
            "description_localisations",
        ],
    ) -> LocaleDict:
        if key == "name_localisations":
            return self.name_localisations
        elif key == "description_localisations":
            return self.description_localisations
        else:
            raise KeyError(key)

    def to_dict(self) -> dict[Literal["name_localisations", "description_localisations"], LocaleDict]:
        return {
            "name_localisations": self.name_localisations,
            "description_localisations": self.description_localisations,
        }
