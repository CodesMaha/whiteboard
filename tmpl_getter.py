# https://github.com/pygame-web/cdn/blob/main/0.9.3/default.tmpl

from pygbag import web
from pygbag.app import DEFAULT_CDN, DEFAULT_TMPL

tmpl_path, _ = web.get(f"{DEFAULT_CDN}/default.tmpl", DEFAULT_TMPL)

with open(tmpl_path, "r+", encoding="utf-8") as f:
    tmpl = f.read().replace(
        "canvas.emscripten {", 
        "canvas.emscripten {\n\t\t\ttouch-action: none;\n\t\t\t"
    )
    f.seek(0); f.write(tmpl)
