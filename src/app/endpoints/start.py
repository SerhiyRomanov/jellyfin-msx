from fastapi import APIRouter, Request

from app.endpoints.utils import build_msx_uri
from msx_models.start import Start
from msx_models.utils import expect_keywords

router = APIRouter()


@router.get("/start.json")
def start_json(request: Request):
    menu_url = build_msx_uri(str(request.url_for("menu_json")))
    return Start(
        name="Jellyfin MSX",
        parameter=f"menu:{expect_keywords(menu_url)}"
    )
