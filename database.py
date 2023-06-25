from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# For write intensive or production environment, db like postgres may be more suitable...
# but for the purpose of this project and ease of installation,
# I use sqlite because it is based off a single file.

# TODO: use a suitable database system to handle application use case
SQLALCHEMY_DATABASE_URL = "sqlite:///./audit_log_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
