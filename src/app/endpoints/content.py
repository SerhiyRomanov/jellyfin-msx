from fastapi import APIRouter, Request

from app.dependencies import JellyFinDep
from app.endpoints.utils import build_msx_uri
from msx_models.content import ContentItem, ContentRoot, Template
from msx_models.utils import add_query_params

router = APIRouter()


@router.get("/content.json")
async def content_json(request: Request, item_id: str, jellyfin_client: JellyFinDep):
    resp_items = await jellyfin_client.request(
        "GET", f"/Items",
        params=dict(
            ParentId=item_id,
            sortBy="DateCreated",
            sortOrder="Descending",
        )
    )

    content_json_url = build_msx_uri(str(request.url_for("content_json")))
    player_json_url = build_msx_uri(
            str(request.url_for("player_json")),
            ["ID", "PLATFORM", "PLAYER"]
    )
    content_items = []

    for item in resp_items["Items"]:
        match item["Type"]:
            case "Folder" | "Series" | "Season" | "BoxSet":
                content_items.append(
                    ContentItem(
                        title=item["Name"],
                        image=jellyfin_client.create_items_image_url(item["Id"], "Primary"),
                        imageFiller="smart",
                        action="content:" + add_query_params(content_json_url, dict(item_id=item["Id"]))
                    )
                )
            case "Movie" | "Episode" | "Video" | "MusicVideo":
                content_items.append(
                    ContentItem(
                        title=item["Name"],
                        image=jellyfin_client.create_items_image_url(item["Id"], "Primary"),
                        imageFiller="smart",
                        action=f"execute:fetch:{add_query_params(player_json_url, dict(item_id=item['Id']))}"
                    )
                )

    return ContentRoot(
        type=ContentRoot.Type.list.value,
        template=Template(layout="0,0,4,3"),
        items=content_items
    )
