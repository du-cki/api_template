from aiohttp.web import Request, Response, StreamResponse, WebSocketResponse
from typing import Awaitable, Callable, Literal, Any


FuncT = Callable[..., Awaitable[Any]]

Method = Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
Handler = Callable[[Request], Awaitable[Response]]

GenericHandler = Callable[[Request], Awaitable[Any]]
ErrorHandler = Callable[[Request, Exception], Awaitable[Any]]

ResponseT = StreamResponse | Response | WebSocketResponse