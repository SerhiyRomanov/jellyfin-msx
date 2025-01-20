from fastapi import APIRouter, Request

from app.dependencies import JellyFinDep
from app.endpoints.utils import build_msx_uri
from msx_models.content import ContentRoot, ContentItem, Template
from msx_models.utils import expect_keywords, add_query_params

router = APIRouter()


@router.get("/home.json")
async def home_json(request: Request, jellyfin_client: JellyFinDep):
    resp = await jellyfin_client.request("GET", "/UserViews")

    content_items = []
    for item in resp["Items"]:
        content_json_url = expect_keywords(build_msx_uri(str(request.url_for("content_json"))))

        content_items.append(
            ContentItem(
                title=item["Name"],
                image=jellyfin_client.create_items_image_url(item["Id"], "Primary"),
                imageFiller="smart",
                action="content:" + add_query_params(content_json_url, dict(item_id=item["Id"]))
            )
        )

    return ContentRoot(
        type=ContentRoot.Type.pages.value,
        template=Template(layout="0,0,6,3"),
        items=content_items
    )
