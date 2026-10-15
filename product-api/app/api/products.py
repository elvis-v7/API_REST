from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductOut, ProductPatch
from app.services.product_service import ProductService

router = APIRouter(prefix="/api/v1/products", tags=["Products"])


def get_service(session: AsyncSession = Depends(get_session)) -> ProductService:
    return ProductService(ProductRepository(session))


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(body: ProductCreate, service: ProductService = Depends(get_service)):
    return await service.create(body.model_dump())


@router.get("/", response_model=list[ProductOut])
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    name: str | None = None,
    service: ProductService = Depends(get_service),
):
    return await service.list(skip, limit, name)


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, service: ProductService = Depends(get_service)):
    return await service.get(product_id)


@router.put("/{product_id}", response_model=ProductOut)
async def replace_product(
    product_id: int, body: ProductCreate, service: ProductService = Depends(get_service)
):
    return await service.replace(product_id, body.model_dump())


@router.patch("/{product_id}", response_model=ProductOut)
async def patch_product(
    product_id: int, body: ProductPatch, service: ProductService = Depends(get_service)
):
    return await service.patch(product_id, body.model_dump(exclude_unset=True))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, service: ProductService = Depends(get_service)):
    await service.delete(product_id)
