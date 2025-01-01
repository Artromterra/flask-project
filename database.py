import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from env_conf import *

db_url = 'postgresql+psycopg2://{user}:{password}@{host}:{port}'.format(
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DB_HOST,
    port=PORT,
)

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()

