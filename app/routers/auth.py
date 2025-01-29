from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta
import bcrypt
from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, EmailStr
from app.core.dependencies import DBDep
from app.core.config import get_settings
from app.models.models import User  # Assurez-vous que votre modèle User est importé

settings = get_settings()

router = APIRouter()

class SignUpReq(BaseModel):
    email: EmailStr
    username: str
    password: str

class SignInReq(BaseModel):
    email: EmailStr
    password: str
    
class UserDB(BaseModel):
    user_id: int
    email: str
    username: str | None
    password: str | None
    is_admin: bool

@router.post("/signup")
def signup(sign_up_req: SignUpReq, db: Session = DBDep):
    hashed = bcrypt.hashpw(sign_up_req.password.encode("utf-8"), bcrypt.gensalt())

    # Vérifier si l'utilisateur existe déjà
    user = db.query(User).filter((User.email == sign_up_req.email) | (User.username == sign_up_req.username)).first()
    
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Créer un nouvel utilisateur
    new_user = User(email=sign_up_req.email, username=sign_up_req.username, password=hashed.decode("utf-8"), is_admin=False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Sign up success"}

@router.post("/signin")
def signin(sign_in_req: SignInReq, response: Response, db: Session = DBDep):
    # Vérifier les champs
    if not sign_in_req.email or not sign_in_req.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    
    # Chercher l'utilisateur par email
    user = db.query(User).filter(User.email.ilike(sign_in_req.email)).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Vérifier le mot de passe
    if not bcrypt.checkpw(sign_in_req.password.encode("utf-8"), user.password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    
    # Créer un token JWT
    expire = datetime.utcnow() + timedelta(minutes=int(settings.JWT_EXPIRATION))
    payload = {"sub": str(user.user_id), "exp": expire, "is_admin": user.is_admin}
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    
    # Ajouter le token dans un cookie HTTP-only
    response.set_cookie(key="jwt", value=token, httponly=True)

    return {"message": "Sign in success"}
