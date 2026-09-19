from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DeviceCreate(BaseModel):

    name: str = Field(
        ...,
        min_length=1,
        examples=["Laptop Lenovo ThinkPad"]
    )

    serial_number: str = Field(
        ...,
        min_length=1,
        examples=["LEN-2024-001"]
    )

    device_type: str = Field(
        ...,
        min_length=1,
        examples=["laptop"]
    )

    brand: str | None = Field(
        default=None,
        examples=["Lenovo"]
    )

    is_available: bool = Field(
        default=True,
        examples=[True]
    )


class DeviceUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        examples=["Laptop Lenovo ThinkPad"]
    )

    serial_number: str | None = Field(
        default=None,
        examples=["LEN-2024-001"]
    )

    device_type: str | None = Field(
        default=None,
        examples=["laptop"]
    )

    brand: str | None = Field(
        default=None,
        examples=["Lenovo"]
    )

    is_available: bool | None = Field(
        default=None,
        examples=[True]
    )


class DeviceResponse(BaseModel):

    id: int
    name: str
    serial_number: str
    device_type: str
    brand: str | None = None
    is_available: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )