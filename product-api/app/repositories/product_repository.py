from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product


class ProductRepository:
    """Capa de acceso a datos: solo consultas asíncronas a la BD."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: dict) -> Product:
        product = Product(**data)
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def list(self, skip: int, limit: int, name: str | None):
        query = select(Product).order_by(Product.id).offset(skip).limit(limit)
        if name:
            query = query.where(Product.name.ilike(f"%{name}%"))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, product_id: int) -> Product | None:
        result = await self.session.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()

    async def get_by_sku(self, sku: str) -> Product | None:
        result = await self.session.execute(select(Product).where(Product.sku == sku))
        return result.scalar_one_or_none()

    async def update(self, product: Product, data: dict) -> Product:
        for key, value in data.items():
            setattr(product, key, value)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete(self, product: Product) -> None:
        await self.session.delete(product)
        await self.session.commit()
