from fastapi import FastAPI
from dexbooruml.routers.tags import build_tag_router
from dexbooruml.routers.general import build_general_router
import os

# define application routers
tags_router, tags_router_tag = build_tag_router()
general_router, general_router_tag = build_general_router()

# define main application instance and routers
app = FastAPI(title='Dexbooru ML API')
app.include_router(router=tags_router, prefix='/api/tags', tags=[tags_router_tag])
app.include_router(router=general_router, prefix='/api/general', tags=[general_router_tag])


