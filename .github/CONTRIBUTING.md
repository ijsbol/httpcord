# HTTPCord Contributor Guidelines

This serves as guideline on how to correctly contribute to the HTTPCord library.

This exists to reduce the number of unnecessary code reviews I have to do, allowing me to drink more Arizona Iced Green Tea & Honey.


## Guidelines

#### 0. Use atomic-commits.

If I see a `changed some things | -143 +1042` I am going to close your PR.

Use [atomic commit styling](https://medium.com/@krystalcampioni/advanced-git-guide-part-1-mastering-atomic-commits-and-enforcing-conventional-commits-1be401467a92). This means using `feat: description of a feature here`, `fix: description of bug fixed here`, etc. Along side smalllllllll commit sizes, unless it's otherwise impossible.

Remember, people will see these commit messages and will try to figure out what you are doing. Be helpful.

#### 1. Type-hint everything according to PEP-8 and PyRight. There are two exceptions to this rule.
- Untyped or improperly typed code will be met with indefinite PR comments until fixed.
- Common things that annoy me and will result in PR comments until fixed:
    - `typing.Optional`: Use `<type> | None` instead of `typing.Optional[<type>]`.
    - `typing.Union`: Use `<type> | <other type>` instead of `typing.Union[<type>, <other type>]`.
    - Untyped `__init__` functions. Please type them as `-> None`.

##### Exceptions
`__slots__` & `__all__` -> Must be explicitly typed as `tuple[str, ...]` despite being implicitly typed this way by all type-checkers.

*Why? Because I like it this way.
[I am objectively correct in all instances and people should capitulate to my whimsical whims if they wish to engage](https://discord.com/channels/721528373377105970/1378440281678151833/1387453789233217647).*


#### 2. Test. Your. Code.
- If you submit code that has a syntax error in, I am closing the PR.
- If someone's client breaks because of code you submitted, I will `git blame` you <3


#### 3. Discuss PRs in [#httpcord-discussions](https://discord.com/channels/721528373377105970/1378440281678151833) on our [support server](https://discord.gg/yfY5XASZ85).

Your PR idea may already be being implemented by someone, check!


#### 4. Use `@property` decorators on class attributes, and have the actual attribute private.

Yes, I am aware we [don't follow this in some sections of the library](https://github.com/ijsbol/httpcord/blob/main/httpcord/attachment.py).

This is something that will be fixed, eventually:tm:


#### 5. Please comment your code, *where necessary*.

This means doc-strings on classes and methods, and comments on complex / not immediately understandable sections of code. Under-commenting is bad, over-commenting is worse.


### Example of a nicely typed ready-to-merge code segment.
```python
__all__: tuple[str, ...] = (
    "Thing",
)


class Thing:
    """ A class that stores a thing and can optionally return said thing. """

    __slots__: tuple[str, ...] = (
        "_thing",
    )

    def __init__(self, thing: int) -> None:
        self._thing: int = thing

    @property
    def thing(self) -> int:
        return self._thing
```