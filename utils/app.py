import functools

from aiohttp import web
from importlib import import_module

from typing import TYPE_CHECKING, Optional

from .logger import logger

if TYPE_CHECKING:
    from .types import Route, METHODS, HANDLER


def construct_route(path: str) -> str:
    raw_path = path.split(".")[1:]  # removes the module name (i.e `routes`)
    if raw_path[-1:][0] == "index":
        return "/" + "/".join(raw_path[:-1])

    return "/" + "/".join(raw_path)


class App(web.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_startup.append(self.on_ready)

    async def on_ready(self, _app: web.Application):
        logger.info("Hello, World!")

    def load_extension(self, extension: str, *, silent: bool = False):
        try:
            mod = import_module(extension)
        except ModuleNotFoundError:
            if not silent:
                raise Exception(f"Extension {extension} not found.")

            logger.error(f"Extension {extension} not found.")
        else:
            routes: Optional[list["Route"]] = vars(mod).get("__APP_ROUTES")

            if routes is None:
                logger.warning(
                    f"Tried to load {extension} but it didn't contain any `@route`s."
                )
                return

            for route in routes:
                path = route["path"] or construct_route(extension)
                self.router.add_route(
                    route["method"],
                    path,
                    route["handler"],
                )

                logger.info(f"Loaded {path}")


def route(
    *,
    method: Optional["METHODS"] = "GET",
    path: Optional[
        str
    ] = None,  # by default, it will be the file based routing, but this will override it if needed.
    name: Optional[str] = None,  # name of route, defaults to the path.
):
    def wrapper(f: "HANDLER"):
        methods = f.__globals__.setdefault("__APP_ROUTES", [])
        methods.append({"path": path, "method": method, "name": name, "handler": f})

        @functools.wraps(f)
        async def wrapped(*args):
            return await f(*args)

        return wrapped

    return wrapper
