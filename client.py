"""
MCP Client that connects to the FastAPI-hosted server over Streamable HTTP.

Run the server first (uvicorn server:app --port 8000), then:
    python client.py
"""

import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

SERVER_URL = "http://localhost:8000/mcp"


async def main() -> None:
    # 1. Open the transport, then an MCP session on top of it
    async with streamable_http_client(SERVER_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 2. Discover what the server offers
            tools = await session.list_tools()
            print("Tools available:")
            for t in tools.tools:
                print(f"  - {t.name}: {t.description.splitlines()[0]}")

            # 3. Call a tool: search products by retailer and category
            result = await session.call_tool(
                "get_products",
                {
                    "retailer_code": ["SR"],
                    "category": ["Bebidas"],
                    "limit": 5,
                },
            )
            print("\nget_products(retailer_code=['SR'], category=['Bebidas'], limit=5):")
            print(" ", result.content[0].text)

            # 4. Another tool: count products matching a filter
            result = await session.call_tool(
                "get_products_count",
                {"retailer_code": ["SR"], "category": ["Bebidas"]},
            )
            print("\nget_products_count(retailer_code=['SR'], category=['Bebidas']):")
            print(" ", result.content[0].text)

            # 5. Read resources
            res = await session.read_resource("retailers://supermarket")
            print("\nResource retailers://supermarket:")
            print(" ", res.contents[0].text)

            res = await session.read_resource("categories://supermarket")
            print("\nResource categories://supermarket:")
            print(" ", res.contents[0].text)


if __name__ == "__main__":
    asyncio.run(main())
