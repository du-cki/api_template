from aiohttp import web

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..app import App


async def handler(_request: web.Request):
    return web.json_response({
        "message": "Pong!"
    })


def setup(app: "App"):
    app.router.add_get("/ping", handler)
