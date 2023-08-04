import logging
from logging import Formatter

colours = {
    "grey": "\x1b[38;20m",
    "yellow": "\x1b[33;20m",
    "purple": "\x1b[35;20m",
    "black": "\x1b[30;20m",
    "red": "\x1b[31;20m",
    "bold_red": "\x1b[31;1m",
    "end": "\x1b[0m",
}


def apply_colour(fmt: str, colour: str) -> Formatter:
    return Formatter(fmt.format(colour=colour, **colours))


class ColourFormatter(Formatter):
    def __init__(
        self,
        *args,
        fmt: str = "{black}%(asctime)s{end} {colour}%(levelname)s{end} ({purple}%(filename)s:%(lineno)d{end}): {colour}%(message)s{end}",
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.fmt = fmt

        self.FORMATS = {
            logging.DEBUG: apply_colour(self.fmt, colours["grey"]),
            logging.INFO: apply_colour(self.fmt, colours["grey"]),
            logging.WARNING: apply_colour(self.fmt, colours["yellow"]),
            logging.ERROR: apply_colour(self.fmt, colours["red"]),
            logging.CRITICAL: apply_colour(self.fmt, colours["bold_red"]),
        }

    def format(self, record):
        fmt = self.FORMATS.get(
            record.levelno,
            apply_colour(
                self.fmt, colours["grey"]
            ),  # won't ever get applied but for linting sake.
        )
        return fmt.format(record)



logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setFormatter(ColourFormatter())

logger.addHandler(ch)
