from sqlalchemy_mixins import AllFeaturesMixin
from sqlalchemy_mixins.timestamp import TimestampsMixin

from src.services.db import base, engine, session


class BaseModel(base, AllFeaturesMixin, TimestampsMixin):
    __abstract__ = True

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def get(cls, **kwargs):
        instance = cls.where(**kwargs).all()
        return instance[0] if len(instance) else None

    @classmethod
    def referent(cls):
        return cls.__name__

    @classmethod
    def tablename(cls):
        return cls.__table__.name

    @classmethod
    def get_foreign_attr(cls, key):
        return f"{cls.tablename()}.{key}"

    @classmethod
    def create(cls, **kwargs):
        columns = [
            col.name.replace("_id", "")
            for col in cls.__table__.columns
            if col.name.endswith("_id")
        ]
        for column in columns:
            if column in kwargs:
                data = kwargs.pop(column)
                kwargs[f"{column}_id"] = data.id

        return super().create(**kwargs)


base.metadata.create_all(engine)
BaseModel.set_session(session)
