import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from fastapi.testclient import TestClient
from app.main import app  # Assurez-vous que votre instance FastAPI est importée correctement
import pytest

client = TestClient(app)

# Test de la création de post
@pytest.fixture
def test_create_post():
    data = {
        "user_id": 1,
        "categorie_id": 2,
        "title": "Test Post",
        "content": "This is a test post",
        "status": "public",
        "published_at": "2025-01-01T00:00:00",
        "updated_at": "2025-01-01T00:00:00"
    }
    
    response = client.post("/posts/", json=data)
    
    # Vérifiez que la réponse a un statut 200
    assert response.status_code == 200
    
    # Vérifiez que le titre du post correspond à celui envoyé dans la requête
    assert response.json()["title"] == "Test Post"
    assert response.json()["status"] == "public"

# Test de la récupération des posts publics
def test_get_public_posts():
    response = client.get("/posts/")
    
    # Vérifiez que la réponse est valide
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Assurez-vous que la réponse est une liste de posts
