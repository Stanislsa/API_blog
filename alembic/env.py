import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Importez Base et vos modèles depuis app.models
from app.models.models import Base  # Assurez-vous que ce chemin est correct
from app.models.models import *  # Cela importe tous vos modèles (Category, User, Post, etc.)

# Configuration de la base de données
from app.config import get_settings

settings = get_settings()
DATABASE_URL = f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Configurer le logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Lier les métadonnées des modèles
target_metadata = Base.metadata  # Cela devrait maintenant être correct

def run_migrations_offline():
    """Configurer les migrations hors ligne."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Configurer les migrations en ligne."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
