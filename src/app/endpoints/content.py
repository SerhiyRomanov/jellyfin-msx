from typing import Dict, List

from fastapi import APIRouter, Request

from app.dependencies import JellyFinDep
from app.endpoints.utils import build_msx_uri
from msx_models.content import ContentItem, ContentRoot, Template
from msx_models.utils import add_query_params

router = APIRouter()


class ContentBuilder:
    content_json_url: str
    player_json_url: str
    jellyfin_client: JellyFinDep

    def __init__(self, jellyfin_client, request: Request):
        self.jellyfin_client = jellyfin_client
        self.content_json_url = build_msx_uri(str(request.url_for("content_json")))
        self.player_json_url = build_msx_uri(
            str(request.url_for("player_json")),
            ["ID", "PLATFORM", "PLAYER"]
        )

    def build(self, items: List[Dict]) -> ContentRoot:
        all_episodes = all(item["Type"] == "Episode" for item in items)

        if all_episodes:
            return self._build_episodes_list(items)

        content_items = []
        for item in items:
            match item["Type"]:
                case "Series" | "Season" | "BoxSet":
                    content_items.append(
                        ContentItem(
                            title=item["Name"],
                            titleFooter=str(item.get("ProductionYear", "")),
                            image=self.jellyfin_client.create_items_image_url(item["Id"], "Primary"),
                            imageFiller="smart",
                            action="content:" + add_query_params(self.content_json_url, dict(item_id=item["Id"]))
                        )
                    )
                case "Movie" | "Video" | "MusicVideo":
                    content_item = ContentItem(
                        title=item["Name"],
                        titleFooter=str(item.get("ProductionYear", "")),
                        image=self.jellyfin_client.create_items_image_url(item["Id"], "Primary"),
                        imageFiller="smart",
                        action=f"execute:fetch:{add_query_params(self.player_json_url, dict(item_id=item['Id']))}"
                    )

                    content_items.append(content_item)

        return ContentRoot(
            type=ContentRoot.Type.pages.value,
            template=Template(layout="0,0,3,6"),
            items=content_items
        )

    def _build_episodes_list(self, items: List[Dict]) -> ContentRoot:
        content_items = []
        for item in items:
            index = f"{item['IndexNumber']}. " if item.get("IndexNumber") else ""
            content_item = ContentItem(
                title=f"{index}{item["Name"]}",
                image=self.jellyfin_client.create_items_image_url(item["Id"], "Primary"),
                imageFiller="smart",
                action=f"execute:fetch:{add_query_params(self.player_json_url, dict(item_id=item['Id']))}"
            )
            content_items.append(content_item)

        return ContentRoot(
            type=ContentRoot.Type.list.value,
            template=Template(layout="0,0,12,2"),
            items=content_items
        )


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

    content_builder = ContentBuilder(jellyfin_client, request)
    content_root = content_builder.build(resp_items["Items"])

    return content_root
