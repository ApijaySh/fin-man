from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from finman_core.config.settings import AppSettings

DATABASE_URL = f"sqlite:///{AppSettings.DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()