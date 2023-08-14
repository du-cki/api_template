from aiohttp import web
from utils import route

@route()
async def handler(_: web.Request):
    return web.json_response({
        "message": "Pong!"
    })
