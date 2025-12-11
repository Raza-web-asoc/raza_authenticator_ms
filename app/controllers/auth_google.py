from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.db.models import User
from app.core.tokenConfig import create_access_token
from app.core.settings import settings

router = APIRouter()

class GoogleToken(BaseModel):
    token: str


async def login_with_google(body: GoogleToken, db: AsyncSession):
    """
    Verifica token de Google enviado desde el frontend, crea el usuario si no existe
    y devuelve un access_token de la aplicación.
    """
    try:
        client_id = settings.google_client_id
        if not client_id:
            raise RuntimeError("Google client id not configured")
        google_info = id_token.verify_oauth2_token(
            body.token,
            google_requests.Request(),
            client_id
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Google token")

    email = google_info.get("email")
    given_name = google_info.get("given_name") or google_info.get("name")
    family_name = google_info.get("family_name", "")
    google_sub = google_info.get("sub")

    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email not provided by Google")

    # Buscar usuario por email
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        # Crear nuevo usuario usando los campos reales del modelo
        user = User(
            username=email.split("@")[0],
            names=given_name,
            last_names=family_name,
            email=email,
            password_hash=None,
            google_id=google_sub
        )
        db.add(user)
        try:
            await db.commit()
            await db.refresh(user)
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error creating user: {str(e)}")
    else:
        # Si existe pero no tiene google_id, actualizarlo
        if not getattr(user, "google_id", None) and google_sub:
            try:
                user.google_id = google_sub
                db.add(user)
                await db.commit()
                await db.refresh(user)
            except Exception:
                await db.rollback()

    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "role": user.role, "user": {"id": user.id_user, "email": user.email, "username": user.username}}


@router.post("/google")
async def login_with_google_endpoint(body: GoogleToken, db: AsyncSession = Depends(get_db)):
    """
    Endpoint para login con Google.
    Recibe token de Google y devuelve JWT de la app.
    """
    return await login_with_google(body, db)


@router.post("/google/signup")
async def signup_with_google(body: GoogleToken, db: AsyncSession = Depends(get_db)):
    """
    Endpoint para signup con Google (reutiliza lógica de login).
    """
    return await login_with_google(body, db)
# ...existing code...