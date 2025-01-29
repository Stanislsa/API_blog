# Utiliser une image de base Python
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires pour installer les dépendances
COPY requirements.txt ./

# Install system dependencies for psycopg
RUN apt-get update && apt-get install -y libpq-dev && apt-get install -y netcat-openbsd

# Installer les dépendances du projet
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers du projet
COPY . .

# Appliquer les migrations de la base de données
# RUN alembic upgrade head

# Exposer le port que FastAPI utilise (par défaut 8000)
EXPOSE 8000

# Commande pour démarrer l'application FastAPI
CMD ["uvicorn", "app.core.main:app", "--host", "0.0.0.0", "--port", "8000"]