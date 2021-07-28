from typing import List, NoReturn, Optional, Union

from src.models import orm
from src.models.parsers import Transactions
from src.utils import get_datetime_lazy


class TransactionToSqlAlchemy:
    """
    Layer between database and kaspi web service
    """

    def __init__(self, transactions: Optional[Transactions] = None) -> None:
        self.model = orm.Transaction
        self.transactions = transactions

    def set(self, transactions: Transactions) -> None:
        self.transactions = transactions

    def load(self) -> Union[List[orm.Transaction], NoReturn]:
        """
        Convert kaspi Transaction instances into sqlalchemy Transaction
            instances

        :return: Converted sqlalchemy Transaction instances
        """
        items = []
        if self.transactions is None:
            raise ValueError("transactions can not be None")

        for item in self.transactions.data:
            for operation in item.data:
                instance = self.model().fill(
                    hash=self.model.get_hash(
                        subject=operation.subject,
                        type_=operation.type,
                        cost=operation.cost,
                    ),
                    subject=operation.subject,
                    type=operation.type,
                    cost=operation.cost,
                    made_date=get_datetime_lazy(
                        day=operation.day, month=operation.month, year=operation.year
                    ),
                )
                items.append(instance)
        return items

    def bulk_create(
        self, items: Optional[List[orm.Transaction]] = None
    ) -> List[orm.Transaction]:
        """
        Create transaction info in database
        :param items: List of Transaction model instances
        :return: List of created Transaction model instances
        """
        if items is None:
            items = self.load()

        results = []
        for item in items:
            results.append(item.save())
        return results

    def bulk_create_if_not_exist(
        self, items: Optional[List[orm.Transaction]] = None
    ) -> List[orm.Transaction]:
        """
        Create transaction info in database if it's not exist
        :param items: List of Transaction model instances
        :return: List of created Transaction model instances
        """
        if items is None:
            items = self.load()

        results = []
        for item in items:
            item_hash = orm.Transaction.get_hash(
                subject=item.subject, type_=item.type, cost=item.cost
            )
            if self.model.get(hash=item_hash) is None:
                results.append(item.save())
        return results
