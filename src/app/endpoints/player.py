from fastapi import APIRouter, Request

from app.dependencies import JellyFinDep
from msx_models.response import Response, ResponseBody
from msx_models.plugins.play_plugin import PlayPlugin

router = APIRouter()


@router.get("/player.json")
async def player_json(request: Request, item_id: str, platform: str, player: str, jellyfin_client: JellyFinDep):
    # TODO: Use platform/player parameters to serve supported container for different platforms

    url = jellyfin_client.create_videos_stream_url(
        item_id,
        container="mp4",
        params=dict(
            static="true",
        )
    )

    play_plugin = PlayPlugin()
    return Response(
            response=ResponseBody(data=dict(
                action=play_plugin.build_action(url)
            ))
    )

