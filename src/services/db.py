import json

import sqlalchemy
from inflect import engine as pluralization_engine
from sqlalchemy import TEXT, Column, Integer, TypeDecorator, create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.mutable import MutableDict, MutableList
from sqlalchemy.orm import scoped_session, sessionmaker

from settings import DB_URL


class Base:
    @declared_attr
    def __tablename__(cls):  # noqa
        return pluralization_engine().plural(cls.__name__.lower())

    id = Column(Integer, autoincrement=True, primary_key=True)


engine: sqlalchemy.engine.base.Engine = create_engine(DB_URL, pool_recycle=3600)
session_factory: sqlalchemy.orm.session.sessionmaker = sessionmaker(
    bind=engine, autocommit=True
)
session = scoped_session(session_factory)
base = declarative_base(cls=Base)


class JSONEncodedDict(TypeDecorator):  # noqa
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is None:
            return None

        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if not value:
            return None

        return json.loads(value)


JsonType = MutableDict.as_mutable(JSONEncodedDict)
ListType = MutableList.as_mutable(JSONEncodedDict)
