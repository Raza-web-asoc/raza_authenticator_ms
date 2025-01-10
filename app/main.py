from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import auth, userController
from app.db.database import init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Orígenes permitidos
    allow_credentials=True,                  # Permitir cookies/autenticación
    allow_methods=[""],                     # Permitir todos los métodos HTTP
    allow_headers=[""],                     # Permitir todos los encabezados
)

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(auth.router, prefix="", tags=["auth"])
app.include_router(userController.router, prefix="/user", tags=["update user"])