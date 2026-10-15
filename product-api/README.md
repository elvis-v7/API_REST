# Product API – API RESTful asíncrona con FastAPI

Microservicio de catálogo de productos e inventario. Evaluación sumativa 1.5 – Arquitectura Orientada a Servicios.

## Tecnologías
- FastAPI
- SQLAlchemy 2.0 (async) + `aiosqlite` (SQLite). Cambiable a PostgreSQL con `asyncpg`.
- Pydantic v2

## Arquitectura en capas

```
Cliente → Router (api/) → Service (services/) → Repository (repositories/) → Base de datos
```

| Carpeta | Responsabilidad |
|---|---|
| `app/api` | Routers HTTP. Sin lógica de BD. |
| `app/services` | Reglas de negocio (SKU único, existencia) y excepciones HTTP. |
| `app/repositories` | Acceso a datos con `AsyncSession`, `select()`, `execute()`, `commit()`. |
| `app/models` | Modelos ORM (SQLAlchemy 2.0). |
| `app/schemas` | DTOs de entrada/salida (Pydantic). |
| `app/core` | Motor async, sesión y conexión. |

## Instalación y ejecución

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Documentación interactiva (Swagger UI): http://127.0.0.1:8000/docs

## Endpoints (`/api/v1/products`)

| Método | Ruta | Descripción | Código |
|---|---|---|---|
| POST | `/` | Crear producto (SKU único) | 201 / 409 / 422 |
| GET | `/?skip=0&limit=10&name=` | Listar con paginación y filtro por nombre | 200 |
| GET | `/{id}` | Obtener por ID | 200 / 404 |
| PUT | `/{id}` | Reemplazo completo | 200 / 404 / 409 / 422 |
| PATCH | `/{id}` | Actualización parcial | 200 / 404 / 409 / 422 |
| DELETE | `/{id}` | Eliminar | 204 / 404 |

## Pruebas con PowerShell + curl.exe

Con el servidor corriendo, en otra terminal:

```powershell
.\tests.ps1
```

Si PowerShell bloquea el script: `Set-ExecutionPolicy -Scope Process Bypass`

Ejemplo (los `\"` escapan las comillas en PowerShell):

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/v1/products/ -H "Content-Type: application/json" -d "{\"sku\":\"A001\",\"name\":\"Mouse\",\"price\":150.5,\"stock\":20}"
```

## Integrantes
- (Agregar nombres del equipo)
