# Retrosynthesis MCP Server

This project implements a Streamable HTTP MCP server for retrosynthesis using FastAPI and AiZynthFinder.

## Setup

1.  **Create and activate a virtual environment (if not already done):**
    ```bash
    uv venv
    source .venv/bin/activate
    ```

2.  **Install dependencies:**
    ```bash
    uv pip install -e .
    uv add "mcp[cli]"
    ```

3.  **Download AiZynthFinder models and data:**
    This will create a `my_aizynth_data` directory and download necessary model files and a `config.yml`.
    ```bash
    mkdir my_aizynth_data
    uv run download_public_data my_aizynth_data
    ```

## Running the Server

To run the server, use uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

*   **GET /**: Basic health check.
    Returns: `{"message": "Retrosynthesis MCP Server is running!"}`

*   **POST /retrosynthesis**: Perform retrosynthesis for a given SMILES string.
    Request Body (JSON):
    ```json
    {
        "smiles": "CCO"
    }
    ```
    Returns: A JSON object containing a list of routes or a message indicating no routes were found.

