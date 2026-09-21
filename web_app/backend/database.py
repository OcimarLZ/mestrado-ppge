import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

CMS_DB_URL = os.getenv("CMS_DB_URL", "sqlite:///./site_cms.db")
MICRODATA_DB_URL = os.getenv("MICRODATA_DB_URL", "sqlite:///d:/Mestrado/Dados/bdados/INEP.db")

# CMS Database Engine
engine = create_engine(
    CMS_DB_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Microdata Database Engine (Read-only queries usually, but handled same way)
microdata_engine = create_engine(
    MICRODATA_DB_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
