from fastapi import FastAPI, status

from event_handler import lifespan

app = FastAPI(title="MCP server", lifespan=lifespan)

@app.get("/health", status_code=status.HTTP_200_OK)
async def health() -> dict[str, str]:
    return {"status": "ok"}

# Mount domain MCPs
from mcp_tools.sales.routes import app as sales_routes

@app.get("/mcp/tools")
def list_tools():
    return [
        {
            "name": "sales",
            "description": "Query sales data using structured intent"
        }
    ]

app.mount("/mcp/tools/sales", sales_routes)
