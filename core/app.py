from __future__ import annotations

from aiohttp import web
from importlib import import_module

from typing import TYPE_CHECKING


from .logger import logger

if TYPE_CHECKING:
    from typing import List, Dict, Any, Optional
    from .route import Route


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
