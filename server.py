"""
MCP Server mounted inside a FastAPI app (Streamable HTTP transport).

The MCP server exposes:
  - Tools:     compound_interest, loan_payment
  - Resource:  rates://central-banks (static reference data)

Run with:
    uvicorn server:app --port 8000
The MCP endpoint will be available at http://localhost:8000/mcp
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from mcp_instance import mcp
import tools.products  # noqa: F401 -- imported for its @mcp.tool() registration

# ---------------------------------------------------------------------------
# 1. Define the MCP server (FastMCP handles the protocol for you)
# ---------------------------------------------------------------------------
# `mcp` lives in mcp_instance.py so tool modules (e.g. tools/products.py) can
# import the same instance without importing server.py itself.


@mcp.tool()
def loan_payment(principal: float, annual_rate: float, years: int) -> dict:
    """Fixed monthly payment for an amortized loan (e.g. mortgage)."""
    r = annual_rate / 12
    n = years * 12
    payment = principal * r / (1 - (1 + r) ** -n) if r else principal / n
    return {
        "monthly_payment": round(payment, 2),
        "total_paid": round(payment * n, 2),
        "total_interest": round(payment * n - principal, 2),
    }


@mcp.resource("rates://central-banks")
def central_bank_rates() -> str:
    """Reference policy rates (static demo data)."""
    return "FED: 4.25% | ECB: 2.15% | BoE: 4.00%"


# ---------------------------------------------------------------------------
# 2. Mount it into a regular FastAPI app
#    The session manager must run for the app's whole lifetime, so we tie it
#    to FastAPI's lifespan.
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp.session_manager.run():
        yield


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