from aiohttp.web import Request, Response
from typing import Awaitable, Callable, Literal, Optional, TypedDict

Methods = Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"] | str
Handler = Callable[[Request], Awaitable[Response]]


class Route(TypedDict):
    method: Methods
    handler: Handler
    path: Optional[str]
    name: Optional[str]
