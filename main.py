"""news-image-20261119 v6: place the pre-rendered entry image in the output.

Stdlib-only launcher. It finds entry.png next to this file and copies it
to MAKEFUN_OUTPUT_DIR (falling back to /output when that directory exists,
otherwise to this file's own directory). No rendering happens here.
"""
import os
import shutil

IMAGE = "entry.png"


def _pick_destination(folder):
    """Return the full path of the image inside `folder`."""
    return os.path.join(folder, IMAGE)


def _output_folder(here):
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if wanted:
        return wanted
    if os.path.isdir("/output"):
        return "/output"
    return here


def run():
    here = os.path.dirname(os.path.abspath(__file__))
    source = _pick_destination(here)
    if not os.path.isfile(source):
        print("missing entry image:", source)
        return 1
    folder = _output_folder(here)
    os.makedirs(folder, exist_ok=True)
    target = _pick_destination(folder)
    if os.path.abspath(source) == os.path.abspath(target):
        print("already in place:", target)
        return 0
    shutil.copyfile(source, target)
    print("wrote", target)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
