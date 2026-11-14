""" load configuration file for usage (only import this) """

from sys import platform
from tomllib import load

emscripten = platform == "emscripten"
try:
    f = open("config.toml", "rb")
except FileNotFoundError:
    f = open("whiteboard/config.toml", "rb")
config: dict[str, dict[str, int]] = load(f); f.close()

colour = {k: (v, v, v) for k, v in config["rgb"].items()}
slider_sv = config["hsv"]
