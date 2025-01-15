from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from env_conf import DATABASE_PASSWORD, DATABASE_USER, DB_HOST, DB_PORT

db_url = 'postgresql+psycopg2://{user}:{password}@{host}:{port}'.format(
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
)

engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()

