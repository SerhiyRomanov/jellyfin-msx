from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import AppConfig
from app.endpoints.router import router

app_config = AppConfig()

print(f"Started with app_config {app_config.model_dump()}")

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# No luck with set up that properly
# app.add_middleware(
#     SessionMiddleware,
#     secret_key=app_config.session_secret_key,
#     max_age=app_config.session_max_age,
#     https_only=True,
#     same_site="none"
# )

app.include_router(router, prefix="/msx")
