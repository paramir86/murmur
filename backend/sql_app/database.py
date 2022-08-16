from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

host = "db:3308"
db_name = "murmur_db"
user = "mysqluser"
password = "mysqlpass"

DATABASE = "mysql://%s:%s@%s/%s" % (
    user,
    password,
    host,
    db_name,
)

ENGINE = create_engine(DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
Base = declarative_base()
