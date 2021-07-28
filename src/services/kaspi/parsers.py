import re
from typing import Optional, Union

from bs4 import BeautifulSoup

from src.models.kaspi import (
    P2PRegexGroups,
    RegexPatterns,
    RegexPatternsItem,
    WOPBRegexGroups,
    WPBRegexGroups,
)
from src.models.parsers import Operations, Transactions

TRANSACTIONS_AS_DICT = dict  # Simple transactions dict represent


def get_operation_type(content) -> str:
    if "Пополнения" in content:
        return "plus"
    return "minus"


def get_regex_proxy_concrete(content: str) -> RegexPatternsItem:
    regex_proxy: RegexPatternsItem = RegexPatterns.WITH_PLUS_BONUS.value

    if "+" not in content:
        regex_proxy = RegexPatterns.WITHOUT_PLUS_BONUS.value

    if any(
        True if item in content else False
        for item in ["Переводы", "В Kaspi Банкомате", "Пополнения"]
    ):
        regex_proxy = RegexPatterns.P2P_TRANSACTIONS.value

    if "DonationAlerts" in content:
        regex_proxy = RegexPatterns.DONATION_ALERTS.value

    if "Отмена" in content:
        regex_proxy = RegexPatterns.CANCELLATIONS.value

    return regex_proxy


def formalize_costs_dict(
    content: str,
) -> Optional[Union[WPBRegexGroups, WOPBRegexGroups, P2PRegexGroups]]:
    _type_: str = get_operation_type(content)
    regex_proxy = get_regex_proxy_concrete(content)

    match = re.match(regex_proxy.pattern, content)
    if match is None:
        return None

    groups = regex_proxy.groups.load(match.groups())
    groups._type_ = _type_

    return groups


def get_transactions(soup: BeautifulSoup) -> Transactions:
    results = []
    current_index = 0
    operation_list = soup.find("section", attrs={"class": "goldOperation__list"})
    total = 0

    for tag in operation_list.childGenerator():
        if tag.name is None:
            continue

        content = " ".join(tag.text.split())
        tmp_dict = Operations(date="", data=[])

        if tag.name == "span":
            tmp_dict.date = content
            results.append(tmp_dict)
            current_index = results.index(tmp_dict)
            continue

        data = formalize_costs_dict(content)
        if data is None:
            continue

        results[current_index].data.append(data)
        total += 1

    return Transactions(data=results, total=total)


def get_card_transactions_from_html(html: Union[str, bytes]) -> Transactions:
    soup = BeautifulSoup(html, "lxml")
    return get_transactions(soup)
