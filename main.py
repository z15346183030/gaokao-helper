import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

from core.data_loader import DataLoader
from core.favorites import FavoritesManager
from core.config import get_api_key, set_api_key
from ai.claude_client import ClaudeClient

app = FastAPI(title="高考择校助手")

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")

data_loader = DataLoader(data_dir)
favorites_mgr = FavoritesManager(os.path.join(data_dir, "favorites.json"))
claude_client = None

def init_claude():
    global claude_client
    api_key = get_api_key()
    if api_key:
        try:
            claude_client = ClaudeClient(api_key)
            claude_client.set_data_context(data_loader)
        except Exception:
            claude_client = None

init_claude()

app.mount("/static", StaticFiles(directory=os.path.join(base_dir, "static")), name="static")


class RecommendRequest(BaseModel):
    province: str
    subject: str
    score: int


class ApiKeyRequest(BaseModel):
    api_key: str


@app.get("/", response_class=HTMLResponse)
async def index():
    with open(os.path.join(base_dir, "templates", "index.html"), "r", encoding="utf-8") as f:
        return f.read()


@app.get("/api/provinces")
async def get_provinces():
    return data_loader.get_province_list()


@app.get("/api/subjects")
async def get_subjects(province: str):
    return data_loader.get_subject_types(province)


@app.get("/api/universities")
async def search_universities(
    name: str = "",
    province: str = "",
    type: str = "",
    tag: str = ""
):
    results = data_loader.search_universities(name, province, type, tag)
    return results


@app.get("/api/universities/{name}")
async def get_university_detail(name: str):
    detail = data_loader.get_university_detail(name)
    if not detail:
        raise HTTPException(status_code=404, detail="大学未找到")
    return detail


@app.post("/api/recommend")
async def recommend(req: RecommendRequest):
    results = data_loader.get_recommendations(req.province, req.subject, req.score)
    return results


@app.get("/api/campus-info/{name}")
async def get_campus_info(name: str):
    if not claude_client:
        raise HTTPException(status_code=400, detail="未配置 API Key，请在设置中配置")

    cached = claude_client.get_cached_campus_info(name)
    if cached:
        return {"university": name, "content": cached, "cached": True}

    content = claude_client.get_campus_info(name)
    return {"university": name, "content": content, "cached": False}


@app.post("/api/config/api-key")
async def configure_api_key(req: ApiKeyRequest):
    set_api_key(req.api_key)
    init_claude()
    return {"success": True, "has_key": claude_client is not None}


@app.get("/api/config/status")
async def config_status():
    return {
        "has_key": get_api_key() != "",
        "ai_ready": claude_client is not None
    }


@app.get("/api/favorites")
async def get_favorites():
    return favorites_mgr.get_all()


@app.post("/api/favorites/{name}")
async def add_favorite(name: str):
    favorites_mgr.add(name)
    return {"success": True}


@app.delete("/api/favorites/{name}")
async def remove_favorite(name: str):
    favorites_mgr.remove(name)
    return {"success": True}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
