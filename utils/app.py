import functools

from aiohttp import web
from importlib import import_module

from typing import TYPE_CHECKING

from .logger import logger

if TYPE_CHECKING:
    from typing import Optional, List, Dict, Any
    from .types import Route, Methods, Handler


class App(web.Application):
    config: "Optional[Dict[str, Any]]"

    def __init__(self, config: "Dict[str, Any]", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.on_startup.append(self.on_ready)

    def __construct_route(self, path: str) -> str:
        raw_path = path.split(".")[1:]  # removes the module name (`routes`)
        if raw_path[-1:][0] == "index":
            return "/" + "/".join(raw_path[:-1])

        return "/" + "/".join(raw_path)

    async def on_ready(self, _: web.Application):
        ...

    def load_extension(self, extension: str, *, silent: bool = False):
        try:
            mod = import_module(extension)
        except ModuleNotFoundError:
            if not silent:
                raise Exception(f"Extension {extension} not found.")

            logger.error(f"Extension {extension} not found.")
        else:
            routes: "Optional[List['Route']]" = vars(mod).get("__APP_ROUTES")

            if routes is None:
                logger.warning(
                    f"Tried to load {extension} but it didn't contain any `@route`s."
                )
                return

            for route in routes:
                path = route["path"] or self.__construct_route(extension)
                self.router.add_route(
                    route["method"],
                    path,
                    route["handler"]
                )

                logger.info(f"Loaded {path}")


def route(
    *,
    method: "Optional['Methods']" = "GET",
    path: "Optional[str]" = None,
):
    """
    Defines a `route` on a file.

    Parameters
    -----------
    method: Methods
        The request method of the route, defaults to `GET`.

    path: Optional[str]
        The path of the route. If not passed, it would be inferred from the file path.
    """
    def wrapper(f: "Handler"):
        methods = f.__globals__.setdefault("__APP_ROUTES", [])
        methods.append({
            "path": path,
            "method": method,
            "handler": f
        })

        @functools.wraps(f)
        async def wrapped(*args):
            return await f(*args)

        return wrapped

    return wrapper
