from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):  # POST y PUT (payload completo)
    sku: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)


class ProductPatch(BaseModel):  # PATCH (todos opcionales)
    sku: str | None = Field(default=None, min_length=1, max_length=50)
    name: str | None = Field(default=None, min_length=1, max_length=100)
    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)


class ProductOut(ProductCreate):  # Respuesta (incluye id)
    model_config = ConfigDict(from_attributes=True)
    id: int
