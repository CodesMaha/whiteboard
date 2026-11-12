""" get (modified) default.tmpl from pygame-web cdn """

# https://github.com/pygame-web/cdn/blob/main/0.9.3/default.tmpl

from pygbag import web
from pygbag.app import DEFAULT_CDN, DEFAULT_TMPL

tmpl_path, _ = web.get(f"{DEFAULT_CDN}/default.tmpl", DEFAULT_TMPL)

with open(tmpl_path, "r+", encoding="utf-8") as f:
    t = "    "; tmpl = f.read().replace(
        "canvas.emscripten {", 
        f"canvas.emscripten {{\n{t*3}touch-action: none;\n{t*3}"
    )
    f.seek(0); f.write(tmpl)
