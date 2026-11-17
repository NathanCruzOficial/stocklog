
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_timeout=5,
    connect_args={
        "connect_timeout": 3,

        # TCP Keepalive
        "keepalives": 1,
        "keepalives_idle": 5,
        "keepalives_interval": 2,
        "keepalives_count": 2,
    },
)

SessionFactory = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db():
    db = SessionFactory()

    try:
        yield db
    finally:
        db.close()
