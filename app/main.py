from fastapi import FastAPI, Request

from app.database.connection import engine, Base
from app.models.user_model import User
from app.routes.user_routes import router as user_router


# Crear las tablas de la base de datos
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Device Systems API",
    description="API REST para la gestión de usuarios del sistema device_systems.",
    version="2.0.0",
    contact={
        "name": "Juan David",
        "email": "juandavidmospa12@gmail.com"
    }
)


@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    response = await call_next(request)

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"

    return response


app.include_router(user_router)


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a Device Systems API"
    }
