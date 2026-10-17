import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL: str | None = os.environ.get("BASE_URL")
    TEST_URL: str | None = os.environ.get("TEST_URL")
    SQLALCHEMY_DATABASE_URL: str | None = os.environ.get("SQLALCHEMY_DATABASE_URL")
    TEST_DATABASE_URL: str | None = os.environ.get("TEST_DATABASE_URL")

