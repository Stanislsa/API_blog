# FastAPI Blog API

Ce projet est une API de blog construite avec **FastAPI**, utilisant **PostgreSQL** et **Docker**.
Il gère les utilisateurs, les articles et les catégories, et inclut l'authentification JWT.

## 🚀 Prérequis
Avant de lancer le projet, assurez-vous d'avoir installé :
- [Python 3.10+](https://www.python.org/downloads/)
- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- [Poetry (optionnel)](https://python-poetry.org/docs/)

## 📌 Configuration du projet

1. **Créer un fichier `.env`** à la racine du projet en se basant sur `.env.template` :
   ```bash
   cp .env.template .env
   ```
2. **Modifier le fichier `.env`** avec vos informations :
   ```env
   DATABASE_URL=postgresql://fastapi:fastapi123@fastapi-db/blog_api_1
   DB_USER=fastapi
   DB_PASSWORD=fastapi123
   DB_HOST=fastapi-db
   DB_PORT=5432
   DB_NAME=blog_api_1
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION=15
   API_KEY=""
   JWT_SECRET=""
   ```
## ⚠ Creer votre propre API_KEY et JWT_SECRET

## 🚀 Installation & Lancement

### 1️⃣ Lancer avec Docker (Recommandé)
```bash
docker compose up --build
```
Cela va démarrer l'API FastAPI et PostgreSQL.

### 2️⃣ Lancer en local (Sans Docker)
1. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Linux/Mac
   venv\Scripts\activate  # Sur Windows
   ```
2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```
3. **Appliquer les migrations**
   ```bash
   alembic upgrade head
   ```
4. **Démarrer le serveur**
   ```bash
   uvicorn app.core.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## 🔗 Documentation API
Une fois l'application démarrée, accédez à la documentation interactive :
- **Swagger UI** : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc** : [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🔥 Commandes utiles
- **Vérifier la connexion Docker** : `docker ps`
- **Recréer les conteneurs** : `docker-compose up --build --force-recreate`
- **Appliquer les migrations** : `alembic upgrade head`
- **Créer une migration** : `alembic revision --autogenerate -m "Migration message"`

## 🛠 Fonctionnalités principales
✅ Authentification JWT (Signup/Login)  
✅ Gestion des utilisateurs (CRUD)  
✅ Gestion des articles de blog (CRUD)  
✅ Gestion des catégories (CRUD)  
✅ Documentation interactive avec Swagger  
✅ Conteneurisation avec Docker  

---
🎯 **À venir** : Commentaires, Likes/Dislikes, Permissions avancées…

🔧 **Auteur** : [Fehizoro](https://github.com/Rakotoarinosy)

