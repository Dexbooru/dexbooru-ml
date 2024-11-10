from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dexbooruml.routers.tags import build_tag_router
from dexbooruml.routers.general import build_general_router
from dexbooruml.routers.posts import build_posts_router
from dexbooruml.config.weaviate_config import vectordb_client
from contextlib import asynccontextmanager
import os

# define application routers
tags_router, tags_router_tag = build_tag_router()
general_router, general_router_tag = build_general_router()
posts_router, posts_router_tag = build_posts_router()

# define application lifespan
@asynccontextmanager
async def app_lifespan(app: FastAPI):
    yield
    vectordb_client.close()

# define main application instance
app = FastAPI(title='Dexbooru ML API', lifespan=app_lifespan)


# bind routers to the application
app.include_router(router=tags_router, prefix='/api/tags', tags=[tags_router_tag])
app.include_router(router=general_router, prefix='/api/general', tags=[general_router_tag])
app.include_router(router=posts_router, prefix='/api/posts', tags=[posts_router_tag])

# add cors middleware
allowed_origins: list[str] = [
    os.getenv('DEXBOORU_WEB_BASE_URL', 'http://localhost:5173')
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)