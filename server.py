"""
MCP Server mounted inside a FastAPI app (Streamable HTTP transport).

The MCP server exposes:
  - Tools:     products://supermarket-products (dynamic data from MongoDB)
  - Resource:  rates://central-banks (static reference data)

Run with:
    uvicorn server:app --port 8000
The MCP endpoint will be available at http://localhost:8000/mcp
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from db import mongo_client, product_repo
from mcp_instance import mcp
import tools.products


@mcp.resource("retailers://supermarket")
def retailers_supermarket_codes() -> str:
    """Reference the codes used by the supermarket products tool to identify retailers."""
    return "Supermercados Rey: SR | Riba Smith = RS | Super Xtra = SX"

@mcp.resource("categories://supermarket")
def categories_supermarket_codes() -> str:
    """Reference the codes used by the supermarket products tool to identify categories."""
    return "Abarrotes,Automotriz,Bebidas,Bebés,Carnes, Aves y Mariscos,Comida Preparada,Confites y Snacks,Congelados,Cuidado Personal y Belleza,Diversión y Entretenimiento,Embutidos y Deli,Farmacia,Ferretería y Herramientas,Frutas y Verduras,Hogar y Belleza,Licores,Lácteos y Huevos,Marca Propia,Mascotas,Moda y Calzado,Panadería,Papelería y Útiles,Perfumes y Fragancias,Pescados y Mariscos,Tecnología,Tierra de Emprendedores,Utensilios y Accesorios"

@asynccontextmanager
async def lifespan(app: FastAPI):
    await product_repo.drop_indexes()
    await product_repo.ensure_indexes()
    async with mcp.session_manager.run():
        yield
    await mongo_client.close()


app = FastAPI(title="Finance API + MCP", lifespan=lifespan)

# Normal REST endpoints coexist with the MCP endpoint
@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


# Mounts the MCP protocol endpoint at /mcp
app.mount("/", mcp.streamable_http_app())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)