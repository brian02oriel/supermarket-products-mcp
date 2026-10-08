# supermarket-products-mcp

Servidor [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) que expone datos de productos de
supermercados panameños (Supermercados Rey, Riba Smith y Super Xtra) almacenados en MongoDB, para que
asistentes como Claude puedan buscarlos, filtrarlos y compararlos.

El servidor MCP corre montado dentro de una app de FastAPI usando transporte Streamable HTTP.

## Arquitectura

```
server.py                          # App FastAPI + servidor MCP montado en /mcp 
mcp_instance.py                    # Instancia compartida de FastMCP (evita imports circulares)
db.py                              # Conexión a MongoDB y wiring del repositorio
client.py                          # Cliente de ejemplo para probar el servidor MCP
tools/
  products.py                     # Tools MCP: get_products, get_products_count
repositories/
  products/
    model.py                      # Modelos Pydantic (Product, ProductFilter, ProductSort...)
    repository.py                 # Acceso a la colección de MongoDB
resources/
  data/                           # CSVs de entrada por retailer + listas de categorías exportadas
  scripts/
    load_products.py              # Carga/actualiza productos desde CSV a MongoDB
    export_distinct_field.py      # Exporta valores distintos de un campo (category, sub_category)
```

### Qué expone el servidor MCP

**Tools**
- `get_products(search, retailer_code, category, sub_category, brand, undiscounted_price, price, sort_by, limit)`
  — Busca productos con filtros opcionales.
- `get_products_count(search, retailer_code, category, sub_category, brand, undiscounted_price, price)`
  — Cuenta productos que cumplen los filtros.

**Resources**
- `retailers://supermarket` — códigos de retailer (`SR`, `RS`, `SX`) y su significado.
- `categories://supermarket` — lista de categorías de referencia.

**REST**
- `GET /health` — health check simple, coexiste con el endpoint MCP.

## Entorno

- Python >= 3.12 (fijado en `.python-version`)
- Gestión de dependencias con [`uv`](https://docs.astral.sh/uv/) (`pyproject.toml` + `uv.lock`)
- MongoDB corriendo localmente (por defecto `mongodb://localhost:27017`, base de datos `genie`)

## Instalación

```bash
uv sync
```

## Cargar datos

Los CSV de origen viven en `resources/data/*.csv` (uno por retailer: `rey.input.csv`, `riba.input.csv`,
`xtra.input.csv`). Para cargarlos/actualizarlos en MongoDB (upsert por `retailer_code` + `sku`):

```bash
uv run resources/scripts/load_products.py
```

Usa la variable de entorno `MONGO_URI` si Mongo no corre en `localhost:27017`.

Para regenerar las listas de categorías/subcategorías de referencia (`resources/data/categories.txt`,
`subcategories.txt`) a partir de los valores distintos en la colección:

```bash
uv run resources/scripts/export_distinct_field.py category
uv run resources/scripts/export_distinct_field.py sub_category
```

## Levantar el servidor

```bash
uvicorn server:app --port 8000
```

El endpoint MCP queda disponible en `http://localhost:8000/mcp`.

## Probar con el cliente de ejemplo

Con el servidor corriendo:

```bash
uv run client.py
```

Este cliente lista las tools disponibles, ejecuta una búsqueda y un conteo de ejemplo, y lee ambos resources.

## Conectar desde Claude

Configura el servidor MCP remoto (via `mcp-remote`) en la config de tu cliente MCP:

```json
{
  "mcpServers": {
    "supermarket-products": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "http://localhost:8000/mcp"]
    }
  }
}
```
