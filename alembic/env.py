from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.models.base import Base
from app.core.config import settings  # Import de settings pour accéder à DATABASE_URL
from dotenv import load_dotenv  # Pour charger les variables d'environnement
import os

from app.models.models import *

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Ceci est l'objet Alembic Config, qui fournit un accès
# aux valeurs du fichier .ini en cours d'utilisation.
config = context.config

# Charger DATABASE_URL depuis les variables d'environnement
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL is not set in your .env file")

# Remplacer sqlalchemy.url dans config avec la valeur de DATABASE_URL
config.set_main_option("sqlalchemy.url", database_url)

# Configurer les logs
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Ajoutez le MetaData de vos modèles ici pour activer l'autogénération
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Exécuter les migrations en mode 'offline'.

    Cette méthode configure le contexte avec uniquement une URL
    sans créer d'Engine.
    """
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Exécuter les migrations en mode 'online'.

    Cette méthode crée un Engine et associe une connexion au contexte.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
