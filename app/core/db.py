from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

settings = get_settings()

# Créer un moteur SQLAlchemy
engine = create_engine(settings.DATABASE_URL)

# Configurer la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_conn():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()