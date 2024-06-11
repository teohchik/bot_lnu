from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db?charset=utf8mb4')
engine.connect()
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime(), default=datetime.now)
    last_faculty = Column(String)
    last_course = Column(String)
    last_group = Column(String)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)