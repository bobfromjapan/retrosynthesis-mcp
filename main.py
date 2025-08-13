from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP
import os
import logging
import subprocess
import pandas as pd
from aizynthfinder.aizynthfinder import AiZynthFinder
# Setup logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

mcp = FastMCP("RetroSynthesisMCP")
filename = "data/config.yml"
finder = AiZynthFinder(configfile=filename)
finder.stock.select("zinc")
finder.expansion_policy.select("uspto")
finder.filter_policy.select("uspto")
# Pydantic model for the request body
class RetrosynthesisRequest(BaseModel):
    smiles: str


@mcp.tool()
def retrosynthesis(smiles: str):
    """
    SMILESを受け取り、逆合成解析を行い結果をJson形式で返すツールです。
    """
    try:
        finder.target_smiles = smiles
        finder.tree_search()
        finder.build_routes()
        stats = finder.extract_statistics()
        if stats:
            logger.info("Retrosynthesis completed successfully.")
            return {"message": "Retrosynthesis completed successfully", "stats": stats}
        else:
            logger.info("No routes found.")
            return {"message": "No routes found"}
    except Exception as e:
        logger.error(f"An error occurred during retrosynthesis: {e}", exc_info=True)
        return {"message": "An error occurred during retrosynthesis", "error": str(e)}
    
mcp_app = mcp.streamable_http_app()
app = FastAPI(
    title="Retrosynthesis MCP Server",
    description="A FastAPI server for retrosynthesis using MCP",
    lifespan=mcp_app.router.lifespan_context
)

app.mount(
    "/mcp-server",
    mcp_app,
)

@app.get("/")
async def read_root():
    return {"message": "Retrosynthesis MCP Server is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)