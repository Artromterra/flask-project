import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_USER=os.getenv("DATABASE_USER")
DATABASE_PASSWORD=os.getenv("DATABASE_PASSWORD")
DB_PORT=os.getenv("DB_PORT")
DB_NAME=os.getenv("DB_NAME")
DB_HOST=os.getenv("DB_HOST")
SECRET_KEY=os.getenv("SECRET_KEY")