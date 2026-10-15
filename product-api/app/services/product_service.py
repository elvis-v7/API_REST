from fastapi import HTTPException, status

from app.repositories.product_repository import ProductRepository


class ProductService:
    """Capa de negocio: reglas (SKU único, existencia) y errores HTTP."""

    def __init__(self, repo: ProductRepository):
        self.repo = repo

    async def _get_or_404(self, product_id: int):
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Producto no encontrado")
        return product

    async def _check_sku(self, sku: str, current_id: int | None = None):
        existing = await self.repo.get_by_sku(sku)
        if existing and existing.id != current_id:
            raise HTTPException(status.HTTP_409_CONFLICT, "El SKU ya existe")

    async def create(self, data: dict):
        await self._check_sku(data["sku"])
        return await self.repo.create(data)

    async def list(self, skip: int, limit: int, name: str | None):
        return await self.repo.list(skip, limit, name)

    async def get(self, product_id: int):
        return await self._get_or_404(product_id)

    async def replace(self, product_id: int, data: dict):
        product = await self._get_or_404(product_id)
        await self._check_sku(data["sku"], product_id)
        return await self.repo.update(product, data)

    async def patch(self, product_id: int, data: dict):
        product = await self._get_or_404(product_id)
        if "sku" in data:
            await self._check_sku(data["sku"], product_id)
        return await self.repo.update(product, data)

    async def delete(self, product_id: int):
        product = await self._get_or_404(product_id)
        await self.repo.delete(product)
