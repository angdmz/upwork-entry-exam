from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from exceptions import install_handlers_into_app
from settings import AppSettings
from api import users_router


def get_app(settings: AppSettings, lifespan):

    app = FastAPI(
        title="Upwork entry exam API",
        docs_url="/",
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.api_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(users_router)
    install_handlers_into_app(app)
    return app
