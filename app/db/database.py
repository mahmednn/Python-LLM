from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



SQLALCHAMY_DB_URI = "sqlite:///./test.db"

engine = create_engine(
    url=SQLALCHAMY_DB_URI
    )

session_local = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

