"""news-image-20261119: copy the pre-rendered entry image to the output."""
# Stdlib-only entry: copy the pre-rendered entry.png to the output directory.
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        out_dir = "/output" if os.path.isdir("/output") else here
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    if os.path.abspath(src) == os.path.abspath(dst):
        print("already in place:", dst)
        return
    shutil.copyfile(src, dst)
    print("saved", dst)


if __name__ == "__main__":
    main()
