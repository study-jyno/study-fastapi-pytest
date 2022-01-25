import abc
import re
import functools

from sqlalchemy import create_engine, inspect, event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker

from app import config


def create_sqlite_db_engine():
    SQLALCHAMY_DATABASE_URL = f'sqlite:////{config.ROOT_PATH}/app.db'

    # Test code 에서도 사용하기 때문에 절대 경로로 지정해 준다
    return create_engine(SQLALCHAMY_DATABASE_URL, connect_args={"check_same_thread": False}, pool_pre_ping=True)


def create_mysql_db_engine():
    db_username = config.DATABASE_USER
    db_password = config.DATABASE_PASSWORD
    db_host = config.DATABASE_HOSTNAME
    db_dbname = config.DATABASE_NAME
    db_charset = config.DATABASE_CHARSET

    MYSQL_DATABASE_URL = f'mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_dbname}?charset={db_charset}'

    engine = create_engine(MYSQL_DATABASE_URL, pool_pre_ping=True)
    return engine


DATABASE_TYPE = config.DATABASE_TYPE

if DATABASE_TYPE == 'SQLITE':
    engine = create_sqlite_db_engine()
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, )


    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

elif DATABASE_TYPE == 'MYSQL':
    engine = create_mysql_db_engine()
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, )

SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def resolve_table_name(name):
    """Resolves table names to their mapped names."""
    names = re.split("(?=[A-Z])", name)  # noqa
    return "_".join([x.lower() for x in names if x])


raise_attribute_error = object()


def resolve_attr(obj, attr, default=None):
    """Attempts to access attr via dotted notation, returns none if attr does not exist."""
    try:
        return functools.reduce(getattr, attr.split("."), obj)
    except AttributeError:
        return default


class CustomBase:
    __repr_attrs__ = []
    __repr_max_length__ = 15

    @declared_attr
    def __tablename__(self):
        return resolve_table_name(self.__name__)

    def dict(self):
        """Returns a dict representation of a model."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @property
    def _id_str(self):
        ids = inspect(self).identity
        if ids:
            return "-".join([str(x) for x in ids]) if len(ids) > 1 else str(ids[0])
        else:
            return "None"

    @property
    def _repr_attrs_str(self):
        max_length = self.__repr_max_length__

        values = []
        single = len(self.__repr_attrs__) == 1
        for key in self.__repr_attrs__:
            if not hasattr(self, key):
                raise KeyError(
                    "{} has incorrect attribute '{}' in "
                    "__repr__attrs__".format(self.__class__, key)
                )
            value = getattr(self, key)
            wrap_in_quote = isinstance(value, str)

            value = str(value)
            if len(value) > max_length:
                value = value[:max_length] + "..."

            if wrap_in_quote:
                value = "'{}'".format(value)
            values.append(value if single else "{}:{}".format(key, value))

        return " ".join(values)

    def __repr__(self):
        # get id like '#123'
        id_str = ("#" + self._id_str) if self._id_str else ""
        # join class name, id and repr_attrs
        return "<{} {}{}>".format(
            self.__class__.__name__,
            id_str,
            " " + self._repr_attrs_str if self._repr_attrs_str else "",
        )


class Base(declarative_base(cls=CustomBase)):
    __abstract__ = True

    @abc.abstractmethod
    def get_name_to_log(self):
        pass
