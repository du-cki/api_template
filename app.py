import tomllib

from aiohttp import web
from pathlib import Path

from utils import App

with open("config.toml", "r") as f:
    config = tomllib.loads(f.read())

app = App()

for f in Path("routes").glob(r"**/[!_]*.py"):
    app.load_extension(
        f.as_posix().replace("/", ".")[:-3],
        silent=True
    )

web.run_app(app, port=config["APP_PORT"])
