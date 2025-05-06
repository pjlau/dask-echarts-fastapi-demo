# src/backend/main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .data_processing import load_and_process_data

app = FastAPI()

# Resolve the absolute path to the frontend directory
frontend_dir = Path(__file__).parent.parent / "frontend"

# Mount the frontend directory to serve static files
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# API endpoint to get Sankey data
@app.get("/api/sankey-data")
async def get_sankey_data():
    data_path = Path(__file__).parent.parent.parent / "data" / "energy_flow.csv"
    data = load_and_process_data(data_path)
    return data

# Serve the HTML frontend
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    html_path = frontend_dir / "index.html"
    with open(html_path, "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)