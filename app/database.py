import psycopg
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:prem1234@localhost:5436/fastapi"

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


# for sqlite only do the following commented part
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# while True:
#     try:
#         conn = psycopg.connect(host='localhost', dbname='fastapi', user='postgres', password='prem1234', port = 5436)
#         cur = conn.cursor()
#         print("DB connection successful")
#         break
#     except Exception as e:
#         print("Connecting to DB failed")
#         print("Error:", e)
#         time.sleep(2)