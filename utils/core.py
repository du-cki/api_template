from __future__ import annotations

from aiohttp import web
from importlib import import_module

from typing import TYPE_CHECKING, Awaitable, Callable

from utils.types import GenericHandler

from .logger import logger

if TYPE_CHECKING:
    from typing import Optional, List, Dict, Any
    from .types import Method, Handler, FuncT


class App(web.Application):
    config: Optional[Dict[str, Any]]

    def __init__(self, config: Dict[str, Any], *args, **kwargs):
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
            routes: Optional[List["Route"]] = vars(mod).get("__APP_ROUTES")

            if routes is None:
                logger.warning(
                    f"Tried to load {extension} but it didn't contain any `@route`s."
                )
                return

            for route in routes:
                path = route.path or self.__construct_route(extension)
                self.router.add_route(
                    route.method,
                    path,
                    route.invoke
                )

                logger.debug(f"Loaded {path}")

class Route:
    __before_invoke: Optional[GenericHandler]
    __after_invoke: Optional[GenericHandler]
    __on_error: Callable[[web.Request, Exception], Awaitable[Any]]

    def __init__(
        self,
        handler: Handler,
        *,
        method: Method = "GET",
        path: Optional[str]
    ):
        self.handler = handler
        self.method = method
        self.path = path

    def before_invoke(self, func: GenericHandler) -> Any:
        """
        A decorator that registers a pre-route hook.

        Parameters
        -----------
        func: GenericHandler
            The function to register as the hook.
        """
        self.__before_invoke = func

        return func

    def after_invoke(self, func: GenericHandler) -> Any:
        """
        A decorator that registers a post-route hook.

        Parameters
        -----------
        func: GenericHandler
            The function to register as the hook.
        """
        self.__after_invoke = func

        return func

    def on_error(self, func: Callable[[web.Request, Exception], Awaitable[Any]]) -> Any:
        """
        A decorator that catches any errors raised by the route, used to handle the errors.

        Note: this would eat up all the errors, if used incorrectly, so keep that in mind.

        Parameters
        -----------
        func: FuncT
            The function to register as error handler.
        """
        self.__on_error = func

        return func

    async def invoke(self, *args, **kwargs) -> Any:
        if self.__before_invoke:
            await self.__before_invoke(*args, **kwargs)

        try:
            resp = await self.handler(*args, **kwargs)
        except Exception as err:
            if self.__on_error:
                return await self.__on_error(*args, err) # type: ignore

            raise err

        if self.__after_invoke:
            await self.__after_invoke(*args, **kwargs)

        return resp


def route(
    *,
    method: Method = "GET",
    path: Optional[str] = None,
):
    """
    Defines a `route` on a file.

    Parameters
    -----------
    method: Method
        The request method of the route, defaults to `GET`.

    path: Optional[str]
        The path of the route. If not passed, it would be inferred from the file path.
    """

    def wrapper(func: "Handler"):
        route = Route(func, path=path, method=method)
        func.__globals__.setdefault("__APP_ROUTES", []).append(route)

        return route

    return wrapper
