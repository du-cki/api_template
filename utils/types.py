from aiohttp.web import Request, Response

from typing import Awaitable, Callable, Literal, Optional, TypedDict

METHODS = Literal['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']
HANDLER = Callable[[Request], Awaitable[Response]]

class Route(TypedDict):
     method: METHODS
     handler: HANDLER
     path: Optional[str]
     name: Optional[str]
