from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# CREAR PRÉSTAMO
# ============================================================

class LoanCreate(BaseModel):

    user_id: int = Field(
        ...,
        examples=[1]
    )

    device_id: int = Field(
        ...,
        examples=[3]
    )


# ============================================================
# ACTUALIZAR PRÉSTAMO
# ============================================================

class LoanUpdate(BaseModel):

    return_date: datetime | None = Field(
        default=None,
        examples=["2026-09-20T15:30:00"]
    )

    status: str | None = Field(
        default=None,
        examples=["returned"]
    )


# ============================================================
# RESPUESTA NORMAL
# ============================================================

class LoanResponse(BaseModel):

    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: datetime | None = None
    status: str

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# DATOS BÁSICOS DEL USUARIO
# ============================================================

class UserBasicResponse(BaseModel):

    id: int
    name: str
    email: str

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# DATOS BÁSICOS DEL DISPOSITIVO
# ============================================================

class DeviceBasicResponse(BaseModel):

    id: int
    name: str
    serial_number: str
    device_type: str
    brand: str | None = None

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# DETALLE DEL PRÉSTAMO
# ============================================================

class LoanDetailResponse(BaseModel):

    loan_id: int
    status: str
    loan_date: datetime
    return_date: datetime | None = None

    user: UserBasicResponse
    device: DeviceBasicResponse

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# RESPUESTA UTILIZADA POR LOS ENDPOINTS DE DETALLE
# ============================================================

class LoanDetailCustomResponse(BaseModel):

    loan_id: int
    status: str
    loan_date: datetime
    return_date: datetime | None = None

    user: UserBasicResponse
    device: DeviceBasicResponse

    model_config = ConfigDict(
        from_attributes=True
    )