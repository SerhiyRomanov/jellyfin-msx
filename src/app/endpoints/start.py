from fastapi import APIRouter, Request

from app.endpoints.utils import build_msx_uri
from msx_models.start import Start

router = APIRouter()


@router.get("/start.json")
def start_json(request: Request):
    return Start(
        name="Jellyfin MSX",
        parameter=f"menu:{build_msx_uri(str(request.url_for("menu_json")))}"
    )
