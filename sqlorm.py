from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

"""
# 	SQLAlchemy Turns Python Objects Into Database Entries
#      python3.9 you-get 'https://www.youtube.com/watch?v=AKQ3XEDI9Mw' 
#      https://docs.sqlalchemy.org/en/20/core/connections.html
#       https://docs.sqlalchemy.org/en/20/core/engines.html
#        https://docs.sqlalchemy.org/en/14/errors.html

/Volumes/work/dev
python3.9 -m pip install virtualenv

mkdir sqlorm; cd sqlorm; virtualenv venv; source venv/bin/activate

cd /Volumes/work/dev/sqlorm/; virtualenv venv; source venv/bin/activate

# virtualenv venv --system-site-packages  ---- to also inherit globally installed packages

source venv/bin/activate
deactivate

python3.9 -m pip install --upgrade pip
python3.9 -m pip install install sqlalchemy
python3.9 -m pip install install requests

cd /Volumes/work/dev/sqlorm/;  python3.9 sqlorm.py


"""
Base = declarative_base()


class Person(Base):
	__tablename__ = "people"

	ssn = Column("ssn", Integer, primary_key=True)
	firstname = Column("firstname", String)
	lastname = Column("lastname", String)
	gender = Column("gender", CHAR)
	age = Column("age", Integer)

	def __init__(self, ssn, firstname, lastname, gender, age):
		self.ssn = ssn
		self.firstname = firstname
		self.lastname = lastname
		self.gender = gender
		self.age = age

	def __repr__(self):
		return f"({self.ssn}) {self.firstname} {self.lastname} ({self.gender} {self.age})"


class Thing(Base):
	__tablename__ = "things"

	tid = Column("tid", Integer, primary_key=True)
	description = Column("description", String)
	owner = Column(Integer, ForeignKey("people.ssn"))


	def __init__(self, tid, description, owner):
		self.tid = tid
		self.description = description
		self.owner = owner

	def __repr__(self):
		return f">>>>({self.tid}) {self.description} owned by {self.owner}"



if os.path.isfile("people.db"):
	engine_exists = True
	engine = create_engine("sqlite:///people.db", echo=False)  # in-memory = create_engine("sqlite://", echo=True)
else:
	engine = create_engine("sqlite:///people.db", echo=True)  # in-memory = create_engine("sqlite://", echo=True)
	Base.metadata.create_all(bind=engine)
	engine_exists = False

Session = sessionmaker(bind=engine)
session = Session()

if engine_exists:
	pass
else:
	person = Person(12312, "Mike", "Smith", "m", 35)
	session.add(person)
	session.commit()

	p1 = Person(31234, "Anna", "Blue", "f", 32)
	p2 = Person(32423, "Bob", "Blue", "m", 34)
	p3 = Person(45654, "Angela", "Colt", "f", 22)
	session.add(p1)
	session.add(p2)
	session.add(p3)
	session.commit()

	t1 = Thing(1, "car", p1.ssn)
	session.add(t1)
	session.commit()

	t2 = Thing(2, "laptop", p1.ssn)
	t3 = Thing(3, "PS5", p2.ssn)
	t4 = Thing(4, "Tool", p3.ssn)
	t5 = Thing(5, "Book", p3.ssn)
	session.add(t2)
	session.add(t3)
	session.add(t4)
	session.add(t5)
	session.commit()


print('*'*20)
results = session.query(Person).all()
print(results)

print(f'filter:  lastname is Blue {("*"*20)}')
results_filter = session.query(Person).filter(Person.lastname == "Blue")
for r in results_filter:
	print(r)

print(f'filter:  age > 22 {("*"*20)}')
results_filter = session.query(Person).filter(Person.age > 22)
for r in results_filter:
	print(r)


print(f'filter: gender and age {("*"*20)}')
results_filter = session.query(Person).filter(Person.gender =="m").filter(Person.age > 34)
for r in results_filter:
	print(r)


print(f'filter: firstname like "An"  {("*"*20)}')
results_filter = session.query(Person).filter(Person.firstname.like("%An%"))
for r in results_filter:
	print(r)


print(f'filter: firstname in list {("*"*20)}')
results_filter = session.query(Person).filter(Person.firstname.in_(["Anna", "Bob"]))
for r in results_filter:
	print(r)


# ------------------------------------------------
print(f'\nAdded foreign key table...')

print(f'filter: all Things  {("*"*20)}')
results = session.query(Thing).all()
for r in results:
	print(r)

print(f'filter: owned by Anna  {("*"*20)}')
results_filter = session.query(Person, Thing).filter(Thing.owner == Person.ssn).filter(Person.firstname == "Anna").all()
for r in results_filter:
	print(r)


print(f'filter: owned by Anna and Bob {("*"*20)}')
results_filter = session.query(Thing, Person).filter(Thing.owner == Person.ssn).filter(Person.firstname.in_(["Anna", "Bob"])).all()
for r in results_filter:
	print(r)



# end ###

"""

PostgreSQL
The PostgreSQL dialect uses psycopg2 as the default DBAPI. Other PostgreSQL DBAPIs include pg8000 and asyncpg:

# default
engine = create_engine("postgresql://scott:tiger@localhost/mydatabase")

# psycopg2
engine = create_engine("postgresql+psycopg2://scott:tiger@localhost/mydatabase")

# pg8000
engine = create_engine("postgresql+pg8000://scott:tiger@localhost/mydatabase")


MySQL
The MySQL dialect uses mysqlclient as the default DBAPI. There are other MySQL DBAPIs available, including PyMySQL:

# default
engine = create_engine("mysql://scott:tiger@localhost/foo")

# mysqlclient (a maintained fork of MySQL-Python)
engine = create_engine("mysql+mysqldb://scott:tiger@localhost/foo")

# PyMySQL
engine = create_engine("mysql+pymysql://scott:tiger@localhost/foo")


Oracle
The Oracle dialect uses cx_oracle as the default DBAPI:

engine = create_engine("oracle://scott:tiger@127.0.0.1:1521/sidname")

engine = create_engine("oracle+cx_oracle://scott:tiger@tnsname")


Microsoft SQL Server
The SQL Server dialect uses pyodbc as the default DBAPI. pymssql is also available:

# pyodbc
engine = create_engine("mssql+pyodbc://scott:tiger@mydsn")

# pymssql
engine = create_engine("mssql+pymssql://scott:tiger@hostname:port/dbname")


SQLite
SQLite connects to file-based databases, using the Python built-in module sqlite3 by default.

As SQLite connects to local files, the URL format is slightly different. The “file” portion of the URL is the filename of the database. For a relative file path, this requires three slashes:

# sqlite://<nohostname>/<path>
# where <path> is relative:
engine = create_engine("sqlite:///foo.db")


# Unix/Mac - 4 initial slashes in total
engine = create_engine("sqlite:////absolute/path/to/foo.db")

# Windows
engine = create_engine("sqlite:///C:\\path\\to\\foo.db")

# Windows alternative using raw string
engine = create_engine(r"sqlite:///C:\path\to\foo.db")

To use a SQLite :memory: database, specify an empty URL:

engine = create_engine("sqlite://")



>>> os.path.isfile("/etc/password.txt")
True
>>> os.path.isfile("/etc")
False


import pathlib
p = pathlib.Path('path/to/file')
if p.is_file():  # or p.is_dir() to see if it is a directory
    # do stuff

"""
