from aiohttp.web import Request, Response
from typing import Awaitable, Callable, Literal, Any


FuncT = Callable[..., Awaitable[Any]]

Method = Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"] | str
Handler = Callable[[Request], Awaitable[Response]]

GenericHandler = Callable[[Request], Awaitable[Any]]
