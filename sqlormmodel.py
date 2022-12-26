from sqlalchemy import create_engine, Table, ForeignKey, inspect
from sqlalchemy import Column, String, Integer, CHAR, DateTime, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData # enable meta viewing
from datetime import datetime as dt
from uuid6 import uuid6, uuid7, uuid8
from uuid import uuid5, NAMESPACE_DNS
import os

Base = declarative_base()
metadata_obj = MetaData()

DBN = 'users.db'
BASE_DIR=os.path.dirname(os.path.realpath(__file__))
DBN_STRM="sqlite:///:memory:"  # in-memory
DBN_STRF="sqlite:///{BASE_DIR}/{DBN}"  # on filesystem

"""
        cd /Volumes/work/dev/sqlorm/; virtualenv venv; source venv/bin/activate

        cd /Volumes/work/dev/sqlorm/; clear; python3.9 sqlormmodel.py

        https://docs.sqlalchemy.org/en/14/core/metadata.html


python3.9 -m pip install --upgrade pip
python3.9 -m pip install install sqlalchemy
python3.9 -m pip install install uuid6

If all you want is a unique ID, you should probably call uuid1() or uuid4(). 
Note that: 
uuid1() may compromise privacy since it creates a UUID containing the computer’s network address. 
uuid4() creates a random UUID.
UUID versions 6 and 7 - new Universally Unique Identifier (UUID) 
   formats for use in modern applications and databases 
   https://pypi.org/project/uuid6/


"""
def unique_id(username, email):
        return uuid5(
            namespace=NAMESPACE_DNS,
            name=f"user<{username}>:"
            f"email<{email}>:"f"dt<{dt.utcnow()}>:"
        ).hex 

class User(Base):
    __tablename__ = 'users'

    metadata_obj

    uid = Column("uid", String(), primary_key=True)
    username = Column("username", String(25), nullable=False, unique=True)
    email = Column("email", String(), nullable=False, unique=True)
    date_created = Column("date_created", DateTime(), default=dt.utcnow())

    def __init__(self, username, email, date_created=dt.utcnow(),
                  uid=str(uuid8()) ):    # uuid.uuid4().hex
        self.uid = str(unique_id(username,email))
        self.username = username
        self.email = email
        self.date_created = date_created

    def __repr__(self):
        return f'({self.uid}), {self.username} {self.email} {self.date_created}\n'




def schema_tables():
    insp = inspect(engine, False)
    tables = insp.get_table_names()
    print(f'{("*"*20)}\nTables:\n{tables}')

    for t in tables:
        print(f'{("*"*20)}\nIndexes:\n{t} -->{insp.get_indexes(t)}')

        print(f'{("*"*20)}\nColumns of {t}:')
        for t in tables:
            for c in insp.get_columns(t):
                col = ''
                for count, value in enumerate(c):
                    n = len(value)
                    col += ', '+value+':'+str(c[value])
                print(f'{col}')
                col = ''
    print(f'{("*"*20)}\n')



# -----------------------------
if os.path.isfile(DBN):
    engine_exists = True
    engine = create_engine(DBN_STRM, echo=False)  # in-memory = create_engine("sqlite://", echo=True)
else:
    engine = create_engine(DBN_STRM, echo=False)  # in-memory = create_engine("sqlite://", echo=True)
    Base.metadata.create_all(bind=engine)
    engine_exists = False

Session = sessionmaker(bind=engine)
session = Session()

schema_tables()


"""

if __main__ == '__main__{}':
    pass



# -------------------------------------

postgres
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence, Column, Integer

import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Sequence, Integer, create_engine
Base = declarative_base()

def connection():
    engine = create_engine(f"postgresql://postgres:{os.getenv('PGPASSWORD')}@localhost:{os.getenv('PGPORT')}/test")
    return engine

engine = connection()

class Article(Base):
    __tablename__ = 'article'
    seq = Sequence('article_aid_seq', start=1001)
    aid = Column('aid', Integer, seq, server_default=seq.next_value(), primary_key=True)


Example copied from documentation: https://docs.sqlalchemy.org/en/14/dialects/postgresql.html#postgresql-10-and-above-identity-columns

from sqlalchemy import Table, Column, MetaData, Integer, Identity

metadata = MetaData()

data = Table(
    "data",
    metadata,
    Column(
        'id', Integer, Identity(start=42, cycle=True), primary_key=True
    ),
    Column('data', String)
)


"""
