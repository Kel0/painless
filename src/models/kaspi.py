from dataclasses import asdict, dataclass
from enum import Enum
from typing import Optional, Type, Union


@dataclass(frozen=True)
class KaspiLinks:
    login: str = "https://kaspi.kz/entrance?ref=startHeader"
    transactions: str = "https://kaspi.kz/bank/Gold/2"


@dataclass
class RegexGroups:
    @property
    def type(self):
        if not hasattr(self, "_type_"):
            raise ValueError()
        return self._type_  # noqa

    def to_dict(self):
        return asdict(self)


@dataclass
class P2PRegexGroups(RegexGroups):
    subject: str
    cost: float
    day: int
    month: str
    year: int
    datetime: str
    _type_: Optional[str] = None

    @classmethod
    def load(cls, groups):
        return cls(
            subject=groups[0],
            cost=float(groups[1].replace(",", ".").replace(" ", "")),
            day=groups[2],
            month=groups[3],
            year=groups[4],
            datetime=groups[5],
        )


@dataclass
class WPBRegexGroups(RegexGroups):
    subject: str
    cost: float
    bonus: float
    day: int
    month: str
    year: int
    datetime: str
    _type_: Optional[str] = None

    @classmethod
    def load(cls, groups):
        return cls(
            subject=groups[0],
            cost=float(groups[1].replace(",", ".").replace(" ", "")),
            bonus=float(groups[2].replace(",", ".").replace(" ", "")),
            day=groups[3],
            month=groups[4],
            year=groups[5],
            datetime=groups[6],
        )


@dataclass
class WOPBRegexGroups(RegexGroups):
    subject: str
    cost: float
    day: int
    month: str
    year: int
    datetime: str
    _type_: Optional[str] = None

    @classmethod
    def load(cls, groups):
        return cls(
            subject=groups[0],
            cost=float(groups[1].replace(",", ".").replace(" ", "")),
            day=groups[2],
            month=groups[3],
            year=groups[4],
            datetime=groups[5],
        )


@dataclass
class RegexPatternsItem:
    pattern: str
    groups: Union[
        Type[WPBRegexGroups],
        Type[WOPBRegexGroups],
        Type[P2PRegexGroups],
    ]


class RegexPatterns(Enum):
    WITH_PLUS_BONUS = RegexPatternsItem(
        pattern=r"^([\D\d]+)\s-\s([\d,\s]+)\s.\s\+\s([\d,]+)\s.\s[\D]+([\d]+)\s([\D]+)\s([\d]+)\s..\s([\d:]+)",
        groups=WPBRegexGroups,
    )
    WITHOUT_PLUS_BONUS = RegexPatternsItem(
        pattern=r"^([\D\d]+)\s-\s([\d,\s]+)\s.\s\D+([\d]+)\s([\D]+)\s([\d]+)\s..\s([\d:]+)",
        groups=WOPBRegexGroups,
    )
    P2P_TRANSACTIONS = RegexPatternsItem(
        pattern=r"^([\D\d]+)\s\D+\s([\d,\s]+)\s\D+([\d]+)\s([\D]+)\s([\d]+)\s..\s([\d:]+)",
        groups=P2PRegexGroups,
    )
    DONATION_ALERTS = RegexPatternsItem(
        pattern=r"^([\D\d]+)\s-\s([\d,\s]+)\s.\s[\D\d,]+\-\s[\d,]+\s\D+([\d]+)\s([\D]+)([\d]+)\s..\s([\d:]+)",
        groups=WOPBRegexGroups,
    )
    CANCELLATIONS = RegexPatternsItem(
        pattern=r"^([\D\d]+)\s\+\s([\d\s,]+)\s.\s\D+(\d+)\s(\D+)\s(\d+)\s..\s([\d:]+)",
        groups=WOPBRegexGroups,
    )
