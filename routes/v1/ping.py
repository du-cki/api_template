from aiohttp import web

from utils import route, logger

@route()
async def ping(req: web.Request):
    if req.query.get('err') == "true":
        raise Exception

    return web.json_response({
        "message": "Pong!"
    })

@ping.on_error
async def error(_: web.Request, _e: Exception):
    return web.json_response({
        "error": "Something went wrong"
    }, status=400)

@ping.before_invoke
async def before(_: web.Request):
    logger.info('before ping')

@ping.after_invoke
async def after(_: web.Request):
    logger.info('after ping')
