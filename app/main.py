from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.controllers import auth, userController
from app.db.database import init_db
from app.controllers.auth_google import router as google_auth_router

app = FastAPI(title="Raza Authenticator", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

instrumentator = Instrumentator(should_group_status_codes=False).instrument(app)
instrumentator.expose(app, endpoint="/metrics")

@app.on_event("startup")
async def on_startup():
    await init_db()

# Routers
app.include_router(google_auth_router, prefix="/auth", tags=["auth"])
app.include_router(auth.router, prefix="", tags=["auth"])
app.include_router(userController.router, prefix="/user", tags=["update user"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the User API"}
