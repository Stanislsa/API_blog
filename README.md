# BlogAPI - Documentation

Ce projet implémente une API RESTful de blog, développée avec **FastAPI**. L'API permet de gérer des articles, utilisateurs, commentaires, et propose une fonctionnalité d'authentification via **Google**. Le projet fonctionne avec **Python** et utilise des outils comme **Uvicorn** et **Pydantic** pour l'exécution du serveur. Il est également compatible avec **Docker** pour une mise en production simplifiée.

## 🚀 Table des matières
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Lancement de l'application](#-lancement-de-lapplication)
- [Accès à l'API](#-accès-à-lapi)
- [Configuration de l'authentification Google](#-configuration-de-lauthentification-google)
- [Dépannage](#-dépannage)
- [Fonctionnalités principales](#-fonctionnalités-principales)
- [À venir](#-à-venir)

---

## 🚀 Prérequis

Avant de démarrer, assurez-vous que les éléments suivants sont installés sur votre machine :

- **Python 3.8+**  
  Téléchargez Python [ici](https://www.python.org/downloads/).  
  Assurez-vous que `python` et `pip` sont accessibles depuis la ligne de commande :  
  ```bash
  python --version
  pip --version
  ```

- **Git**  
  Si ce n'est pas déjà fait, installez Git depuis [git-scm.com](https://git-scm.com/).

- **Docker & Docker Compose (optionnel)**  
  Si vous souhaitez utiliser Docker, installez-le depuis [docs.docker.com/get-docker/](https://docs.docker.com/get-docker/).

---

## 📌 Installation

### 1. Cloner le dépôt
Cloner ce projet à l'aide de Git :
```bash
git clone https://github.com/Stanislsa/API_blog.git BlogAPI
cd BlogAPI
```

### 2. Créer un environnement virtuel
Il est recommandé d'utiliser un environnement virtuel pour éviter les conflits de dépendances :
```bash
python -m venv venv
```

### 3. Activer l'environnement virtuel
- **Sur Windows** :
  ```bash
  .\venv\Scripts\activate
  ```
- **Sur Linux/Mac** :
  ```bash
  source venv/bin/activate
  ```

Le prompt devrait maintenant afficher `(venv)` pour indiquer que l'environnement est activé.

### 4. Installer les dépendances
Ensuite, installez toutes les dépendances requises à l'aide de `pip` :
```bash
pip install -r requirements.txt
```

Si le fichier `requirements.txt` n'est pas fourni, installez manuellement les principales dépendances :
```bash
pip install fastapi uvicorn pydantic python-dotenv google-auth google-auth-oauthlib
```

---

## 🚀 Lancement de l'application

### 1. Lancer le serveur avec Uvicorn
Exécutez la commande suivante pour démarrer l'application :
```bash
uvicorn app.core.main:app --host 0.0.0.0 --port 8000 --reload
```
- `--reload` : Active le mode de rechargement automatique lors des modifications du code.
- `--host 0.0.0.0` : Permet d'écouter sur toutes les interfaces réseau (utile si vous utilisez un réseau local).

Le serveur démarre sur [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 2. Lancer avec Docker (Optionnel)
Si vous préférez utiliser Docker, exécutez la commande suivante :
```bash
docker-compose up --build
```
Cela va démarrer l'API FastAPI et configurer la base de données PostgreSQL.

---

## 🔗 Accès à l'API

### Documentation interactive avec Swagger
Une fois l'application démarrée, vous pouvez accéder à la documentation interactive de l'API via Swagger UI :
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Explorer l'API avec ReDoc
Vous pouvez également accéder à une documentation au format ReDoc :
[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔐 Configuration de l'authentification Google

L'application utilise l'authentification Google pour permettre aux utilisateurs de se connecter.

### 1. Créer un projet sur Google Cloud Platform
- Allez sur [Google Cloud Console](https://console.cloud.google.com/).
- Créez un projet.
- Activez l'API Google Identity Platform dans votre projet.
- Créez un client OAuth 2.0 et récupérez votre **Client ID** et **Client Secret**.

### 2. Configurer les variables d'environnement
Dans le dossier racine du projet, créez un fichier `.env` et ajoutez les variables suivantes :
```env
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
```

### 3. Vérification de la configuration
Assurez-vous que votre **Google Client ID** et **Client Secret** sont correctement définis et que l'application peut interagir avec l'API Google pour l'authentification.

---

## 🛠 Dépannage

### 1. L'application ne démarre pas
Si l'application ne démarre pas, essayez les étapes suivantes :

- Vérifiez si un autre service n'occupe pas le port 8000 :
  ```bash
  netstat -ano | findstr :8000
  ```
  Si un PID est retourné, terminez le processus avec :
  ```bash
  taskkill /PID [PID] /F
  ```

- Redémarrez l'application avec un autre port :
  ```bash
  uvicorn app.core.main:app --host 127.0.0.1 --port 8080 --reload
  ```

### 2. Erreurs de dépendances
Si vous obtenez une erreur concernant une dépendance manquante, essayez de réinstaller toutes les dépendances :
```bash
pip install --upgrade -r requirements.txt
```

Si vous avez encore des erreurs avec des paquets comme **Pydantic** ou **Google Auth**, installez-les séparément :
```bash
pip install pydantic google-auth google-auth-oauthlib
```

### 3. L'authentification Google échoue
Assurez-vous que vos clés **Google Client ID** et **Client Secret** sont valides. Si vous recevez une erreur 403, cela peut indiquer que l'authentification a échoué, et vous devrez peut-être vérifier la configuration de votre projet Google Cloud.

---

## 🛠 Fonctionnalités principales

✅ **Authentification Google**  
✅ **Gestion des utilisateurs** (CRUD)  
✅ **Gestion des articles de blog** (CRUD)  
✅ **Gestion des commentaires** (CRUD)  
✅ **Documentation interactive** avec Swagger  
✅ **Conteneurisation avec Docker**  

---

## 🎯 À venir

- **Commentaires** : Ajout de fonctionnalités pour gérer les commentaires sur les articles.
- **Likes/Dislikes** : Ajout de fonctionnalités pour liker ou disliker les articles.
- **Permissions avancées** : Gestion des rôles et permissions pour les utilisateurs.

---

## 🔧 Auteur

Ce projet a été développé par [Stanislas](https://github.com/Stanislsa).  
N'hésitez pas à contribuer ou à signaler des problèmes via les [issues](https://github.com/Stanislsa/API_blog/issues).

---

Ce projet vous permet de mettre en place une API complète pour la gestion d'un blog avec un système d'authentification par Google. En suivant ces étapes, vous pouvez facilement exécuter l'application sur votre machine et tester les différentes fonctionnalités offertes par l'API.
