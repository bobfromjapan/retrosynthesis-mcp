from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from mcp.server.fastmcp import FastMCP
import os
import logging
import subprocess
import pandas as pd
from aizynthfinder.aizynthfinder import AiZynthFinder
import rdkit
# Setup logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

mcp = FastMCP("RetroSynthesisMCP")

# Pydantic model for the request body
class RetrosynthesisRequest(BaseModel):
    smiles: str
    
    @validator('smiles')
    def is_valid_smiles(cls, v):
        try:
            mol = rdkit.Chem.MolFromSmiles(v)
            if mol is None:
                raise ValueError("Invalid SMILES string")
            return v
        except Exception as e:
            raise ValueError("Invalid SMILES string") from e


@mcp.tool()
async def retrosynthesis(smiles: str):
    """
    SMILESを受け取り、逆合成解析を行い結果をJson形式で返すツールです。
    Args:
        smiles (str): 解析対象のSMILES文字列
    Returns:
        dict: 逆合成解析の結果を含むJSON形式の辞書
          - message (str): 処理結果のメッセージ
          - stats (dict): 逆合成解析の統計情報
          - route (dict): 最もスコアの高かった逆合成経路の情報
    """
    finder = AiZynthFinder(configfile="data/config.yml")
    finder.stock.select("zinc")
    finder.expansion_policy.select("uspto")
    finder.filter_policy.select("uspto")
    try:
        finder.target_smiles = smiles
        finder.tree_search()
        finder.build_routes()
        stats = finder.extract_statistics()
        route = finder.routes.reaction_trees[0].to_json()

        if stats:
            logger.info("Retrosynthesis completed successfully.")
            return {"message": "Retrosynthesis completed successfully", "stats": stats, "route": route}
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