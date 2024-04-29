from aiohttp import web

from utils import route, logger


@route()
async def ping(req: web.Request):
    return web.json_response(
        {"message": req["response"]},
    )


@ping.on_error
async def error(_: web.Request, err: Exception):
    logger.error("An error occurred:", exc_info=err)

    return web.json_response(
        {"error": "Something went wrong"},
        status=400,
    )


@ping.before_invoke
async def before(req: web.Request):
    if req.query.get("error"):
        raise Exception("Some random error occurred")

    req["response"] = "Ping"
    logger.info("Called before /v1/ping")


@ping.after_invoke
async def after(_: web.Request):
    logger.info("Called after /v1/ping")
