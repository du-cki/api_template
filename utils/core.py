from __future__ import annotations

from aiohttp import web
from importlib import import_module

from typing import TYPE_CHECKING

from utils.types import GenericHandler

from .logger import logger

if TYPE_CHECKING:
    from typing import List, Dict, Any, Awaitable, Callable, Optional
    from .types import Method, Handler


class App(web.Application):
    config: Optional[Dict[str, Any]]

    def __init__(
        self,
        config: Dict[str, Any],
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.config = config
        self.on_startup.append(self.on_ready)

    def _construct_route(
        self,
        path: str,
    ) -> str:
        raw_path = path.split(".")[1:]  # removes the module name (`routes`)
        if raw_path[-1:][0] == "index":
            return "/" + "/".join(raw_path[:-1])

        return "/" + "/".join(raw_path)

    async def on_ready(
        self,
        _: web.Application,
    ): ...

    def load_extension(
        self,
        extension: str,
        *,
        silent: bool = False,
    ):
        try:
            mod = import_module(extension)
        except ModuleNotFoundError as err:
            if not silent:
                raise Exception(f"Extension {extension} not found.")

            logger.error(f"Extension {extension} not found.", exc_info=err)
        else:
            routes: Optional[List[Route]] = vars(mod).get("__APP_ROUTES")

            if routes is None:
                logger.warning(
                    f"Tried to load {extension} but it didn't contain any `@route`s."
                )
                return

            for route in routes:
                path = route.path or self._construct_route(extension)
                self.router.add_route(route.method, path, route.invoke)

                logger.debug(f"Loaded {path}")


class Route:
    _before_invoke: Optional[GenericHandler] = None
    _after_invoke: Optional[GenericHandler] = None
    _on_error: Optional[Callable[[web.Request, Exception], Awaitable[Any]]] = None

    def __init__(
        self,
        handler: Handler,
        *,
        method: Method = "GET",
        path: Optional[str],
    ):
        self.handler = handler
        self.method = method
        self.path = path

    def before_invoke(
        self,
        func: GenericHandler,
    ) -> Any:
        """
        A decorator that registers a pre-route hook.

        Parameters
        -----------
        func: GenericHandler
            The function to register as the hook.
        """
        self._before_invoke = func

        return func

    def after_invoke(
        self,
        func: GenericHandler,
    ) -> Any:
        """
        A decorator that registers a post-route hook.

        Parameters
        -----------
        func: GenericHandler
            The function to register as the hook.
        """
        self._after_invoke = func

        return func

    def on_error(
        self,
        func: Callable[[web.Request, Exception], Awaitable[Any]],
    ) -> Any:
        """
        A decorator that catches any errors raised by the route, used to handle the errors.

        Note: this would eat up all the errors, if used incorrectly, so keep that in mind.

        Parameters
        -----------
        func: FuncT
            The function to register as error handler.
        """
        self._on_error = func

        return func

    async def invoke(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> web.Response | web.StreamResponse:
        try:
            if self._before_invoke:
                before_resp = await self._before_invoke(*args, **kwargs)

                if isinstance(before_resp, web.StreamResponse | web.Response):
                    return before_resp

            resp = await self.handler(*args, **kwargs)

            if self._after_invoke:
                after_resp = await self._after_invoke(*args, **kwargs)

                if isinstance(after_resp, web.StreamResponse | web.Response):
                    return after_resp

            return resp
        except Exception as err:
            if self._on_error:
                return await self._on_error(*args, err)  # type: ignore

            raise err


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
