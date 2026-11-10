# whiteboard
minimalist whiteboard run in the browser.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [features](#features)
- [building](#building)
- [dependencies](#dependencies)
- [license](#license)

<!-- END doctoc -->

# features
this project is still under development, which means new features are still underway!
+ adjusting brush size by scrolling up or down (similar motion to zooming in or out)

# building
although the static build should already be [hosted online](https://mahacodes.codeberg.page/whiteboard/) using [Codeberg Pages](https://docs.codeberg.org/codeberg-pages/), this is a way to rebuild it locally.

first, `cd` to [project directory](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository). to host it on the browser, build it using `pygbag` and click on the resulting page in http://localhost:8000/.
```bash
python -m pygbag src
```
same command with [uv](https://docs.astral.sh/uv/pip/environments/):
```bash
uv run python -m pygbag src
```

> if the build keeps loading indefinitely with the following warning, trying again with administrator permissions might help: `WARNING: wasm mimetype unsupported on that system, trying to correct`.

> if there is undesired scaling applied to the contents, refresh the tab.

alternatively, the [`./src/main.py`](./src/main.py) file can be interpreted natively.

# dependencies
* `pygame-ce` as the graphical library of choice.
* [`pygbag`](https://pygame-web.github.io/wiki/pygbag/) for the ability to run it on the browser.
```
├── pygame-ce v2.5.8
└── pygbag v0.9.3
```

# license
read full gplv3 license [here](./COPYING). 

program used for favicon is [KPix](https://codeberg.org/krush62/KPix) by [@krush62](https://codeberg.org/krush62) ([GitHub link](https://github.com/krush62)).
