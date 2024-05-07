import tomllib

from aiohttp import web
from pathlib import Path

from core import App, logger

with open("config.toml", "r") as f:
    config = tomllib.loads(f.read())


app = App(config=config)


@app.on_ready
async def on_ready(_: App):
    logger.info("app is running on http://localhost:%s", config["APP_PORT"])


@app.on_close
async def on_close(_: App):
    logger.info("app is shutting down")


for f in Path("routes").glob(r"**/[!_]*.py"):
    app.load_extension(
        f.as_posix().replace("/", ".")[:-3],
        silent=True,
    )

if __name__ == "__main__":
    web.run_app(  # type: ignore
        app,
        port=config["APP_PORT"],
    )
