import subprocess
import os
from pathlib import Path
import json
import argparse
import tempfile
import shutil
from fill_emojis import fill_emojis

SELF_DIR = Path(__file__).parent
COLOR_FORMATS = [
    "glyf",
    "glyf_colr_0",
    "glyf_colr_1",
    "cff_colr_0",
    "cff_colr_1",
    "cff2_colr_0",
    "cff2_colr_1",
    "picosvg",
    "picosvgz",
    "untouchedsvg",
    "untouchedsvgz",
    "cbdt",
    "sbix",
]


def make_config(
    *, output_name: str, family: str, color_format: str, paths: list[str]
) -> str:
    return f"""
output_file = {json.dumps(output_name)}
color_format = "{color_format}"
family = {json.dumps(family)}

[axis.wght]
name = "Weight"
default = 400

[master.regular]
style_name = "Regular"
srcs = {json.dumps(paths, indent=2)}

[master.regular.position]
wght = 400
"""


def copy_emojis() -> Path:
    dir = SELF_DIR / "build" / "twemoji"
    shutil.rmtree(dir, ignore_errors=True)
    dir.mkdir(parents=True, exist_ok=True)

    shutil.copytree(SELF_DIR / "twemoji" / "assets" / "svg", dir, dirs_exist_ok=True)
    return dir


def main():
    parser = argparse.ArgumentParser(
        "generate.py", description="Generate a twemoji font"
    )
    parser.add_argument(
        "-o", "--output", help="Output file name (e.g. font.ttf)", required=True
    )
    parser.add_argument("--family", help="The name of the font family", required=True)
    parser.add_argument(
        "color_format",
        help="The format of the glyphs",
        choices=COLOR_FORMATS,
    )
    args = parser.parse_args()

    dist_dir = copy_emojis()
    fill_emojis(dist_dir)

    config = make_config(
        output_name=args.output,
        family=args.family,
        color_format=args.color_format,
        paths=[str(dist_dir / it) for it in os.listdir(dist_dir)],
    )
    with tempfile.NamedTemporaryFile("w", suffix=".toml", delete_on_close=False) as f:
        f.write(config)
        f.close()

        subprocess.run(["nanoemoji", f.name], check=True)


if __name__ == "__main__":
    main()
