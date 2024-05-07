from __future__ import annotations

from typing import TYPE_CHECKING

from .types import (
    GenericHandler,
    ErrorHandler,
    ResponseT,
    Handler,
    Method,
)

if TYPE_CHECKING:
    from typing import Any, Optional


class Route:
    _before_invoke: Optional[GenericHandler] = None
    _after_invoke: Optional[GenericHandler] = None
    _on_error: Optional[ErrorHandler] = None

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
        func: ErrorHandler,
    ) -> Any:
        """
        A decorator that catches any errors raised by the route, used to handle the errors.

        Note: this would eat up all the errors, if used incorrectly, so keep that in mind.

        Parameters
        -----------
        func: ErrorHandler
            The function to register as error handler.
        """
        self._on_error = func

        return func

    async def invoke(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> ResponseT:
        try:
            if self._before_invoke:
                before_resp = await self._before_invoke(*args, **kwargs)

                if isinstance(before_resp, ResponseT):
                    return before_resp

            resp = await self.handler(*args, **kwargs)

            if self._after_invoke:
                after_resp = await self._after_invoke(*args, **kwargs)

                if isinstance(after_resp, ResponseT):
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
    method: Method = "GET"
        The request method of the route, defaults to `GET`.

    path: Optional[str] = None
        The path of the route. If not passed, it would be inferred from the file path.
    """

    def wrapper(func: "Handler"):
        route = Route(func, path=path, method=method)
        func.__globals__.setdefault("__APP_ROUTES", []).append(route)

        return route

    return wrapper
