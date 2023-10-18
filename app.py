"""application.

app/app.py

"""
from titiler.core.errors import DEFAULT_STATUS_CODES, add_exception_handlers

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from titiler.core.factory import TilerFactory
from titiler.mosaic.factory import MosaicTilerFactory
from titiler.mosaic.errors import MOSAIC_STATUS_CODES
from algorithms import algorithms
from osgeo import gdal
import os


app = FastAPI(title="Tititler server with Slope Algorithm")
app = FastAPI()
origins = [
    "http://localhost:5500",
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tiler = TilerFactory(router_prefix="/cog",process_dependency=algorithms.dependency)
mosaic = MosaicTilerFactory(router_prefix="/mosaicjson",process_dependency=algorithms.dependency)
app.include_router(tiler.router,prefix="/cog", tags=["COG"])
app.include_router(mosaic.router,prefix="/mosaicjson", tags=["MosaicJSON"])

add_exception_handlers(app, DEFAULT_STATUS_CODES)
add_exception_handlers(app, MOSAIC_STATUS_CODES)

