from src.services.kaspi.web import KaspiAuth, KaspiTransactions
from src.services.kaspi.db import TransactionToSqlAlchemy
from loggingconfig import setup_logging


setup_logging()
kaspi_auth = KaspiAuth()
kaspi_transactions = KaspiTransactions(kaspi_auth)
transactions_to_sqlalchemy = TransactionToSqlAlchemy()


def get_transactions() -> None:
    transactions = kaspi_transactions.get_transactions()
    transactions_to_sqlalchemy.set(transactions)
    transactions_to_sqlalchemy.bulk_create_if_not_exist()


get_transactions()
