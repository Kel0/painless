from dataclasses import asdict, dataclass
from typing import List, Union

from .kaspi import P2PRegexGroups, WOPBRegexGroups, WPBRegexGroups


@dataclass
class Operations:
    date: str
    data: List[Union[WPBRegexGroups, WOPBRegexGroups, P2PRegexGroups]]


@dataclass
class Transactions:
    data: List[Operations]
    total: int

    def to_dict(self):
        return asdict(self)
