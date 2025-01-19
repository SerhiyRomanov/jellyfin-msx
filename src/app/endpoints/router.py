from fastapi import APIRouter

from .start import router as start_router
from .menu import router as menu_router
from .login import router as login_router
from .home import router as home_router
from .content import router as content_router
from .player import router as player_router


router = APIRouter()
router.include_router(start_router)
router.include_router(menu_router)
router.include_router(login_router)
router.include_router(home_router)
router.include_router(content_router)
router.include_router(player_router)
