from aiohttp import web

from core import (
    route,
    logger,
)


@route()
async def ping(req: web.Request):
    return web.json_response(
        {"message": req["response"]},
    )


@ping.on_error
async def error(_: web.Request, err: Exception):
    # you can do error handling directly here without hassle
    logger.error("An error occurred:", exc_info=err)

    return web.json_response(
        {"error": "Something went wrong"},
        status=400,
    )


@ping.before_invoke
async def before(req: web.Request):
    # the `Route.before_invoke` hook is called before the route is called
    # if you return a web.Response, it will return that instead of calling the route

    if req.query.get("error"):
        # You could also raise an exception within `before` and the
        # route would not be called, and would exit early.
        raise Exception("Some random error occurred")

    # You can assign values to `req`, before the request is even called
    req["response"] = "Ping"
    logger.info(f"Called before {req.path}")


@ping.after_invoke
async def after(req: web.Request):
    # the `Route.after_invoke` hook is called after the route is called
    logger.info(f"Called after {req.path}")
