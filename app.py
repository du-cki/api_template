import logging
import tomllib

from aiohttp import web

from importlib import import_module
from pathlib import Path

logging.basicConfig(format="%(levelname)s | %(asctime)s | %(filename)s: %(message)s")
logger = logging.getLogger("__main__")
logger.setLevel(logging.INFO)

with open("config.toml", "r") as f:
    config = tomllib.loads(f.read())


class App(web.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_startup.append(self.on_ready)

    async def on_ready(self, _app: web.Application):
        logger.info("Hello, World!")

    def load_extension(self, route: str, silent: bool = False):
        try:
            mod = import_module(route)
        except ModuleNotFoundError:
            if silent:
                logger.exception(f"Extension {route} not found.")
                return

            raise Exception(f"Extension {route} not found.")
        else:
            if hasattr(mod, "setup"):
                mod.setup(self)


app = App()

for f in Path("routes").glob(r"**/[!_]*.py"):
    route = f.as_posix().replace("/", ".")[:-3]

    app.load_extension(route, silent=True)
    logger.info(f"Loaded `{route}`")


web.run_app(app, port=config["APP_PORT"])
