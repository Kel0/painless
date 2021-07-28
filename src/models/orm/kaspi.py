from hashlib import md5

from sqlalchemy import TIMESTAMP, Column, Float, String

from .base import BaseModel


class ConfirmCode(BaseModel):
    code = Column(String(length=255))

    @classmethod
    def register_code(cls, code):
        return cls.create(code=code)

    @classmethod
    def check(cls, code: str):
        instance = cls.get(code=code)
        if instance:
            return True
        return False


class Transaction(BaseModel):
    hash = Column(String(length=255))
    subject = Column(String(length=255))
    type = Column(String(length=10))
    cost = Column(Float)
    made_date = Column(TIMESTAMP(timezone=False), nullable=False)

    @classmethod
    def get_hash(cls, subject: str, type_: str, cost: float) -> str:
        to_hash_string = subject + type_ + str(cost)
        return md5(to_hash_string.encode()).hexdigest()
