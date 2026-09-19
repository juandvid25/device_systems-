from fastapi import FastAPI, Request

from app.database.connection import engine, Base

# Importar modelos
from app.models import (
    user_model,
    device_model,
    loan_model
)

# Importar routers
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router


# ============================================================
# CREAR TABLAS
# ============================================================

Base.metadata.create_all(
    bind=engine
)


# ============================================================
# CONFIGURACIÓN FASTAPI
# ============================================================

app = FastAPI(
    title="Device Systems API",
    description=(
        "API REST para la gestión de usuarios, "
        "dispositivos y préstamos del sistema "
        "device_systems."
    ),
    version="2.0.0",
    contact={
        "name": "Juan David",
        "email": "juandavidmospa12@gmail.com"
    }
)


# ============================================================
# MIDDLEWARE
# ============================================================

@app.middleware("http")
async def add_custom_headers(
    request: Request,
    call_next
):

    response = await call_next(request)

    response.headers["X-App-Name"] = "device_systems"

    response.headers["X-API-Version"] = "2.0"

    return response


# ============================================================
# REGISTRAR ROUTERS
# ============================================================

app.include_router(
    user_router
)

app.include_router(
    device_router
)

app.include_router(
    loan_router
)


# ============================================================
# RUTA PRINCIPAL
# ============================================================

@app.get(
    "/",
    tags=["Root"],
    summary="Inicio de la API"
)
def inicio():

    return {
        "mensaje": "Bienvenido a Device Systems API"
    }