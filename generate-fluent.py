import subprocess
import os
import shutil
from pathlib import Path
import json
import argparse
import tempfile
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


TYPE_TO_DIR = {"color": "Color", "flat": "Flat", "high_contrast": "High Contrast"}

SKINTONES = [
    ("Default", ""),
    ("Light", "1f3fb"),
    ("Medium-Light", "1f3fc"),
    ("Medium", "1f3fd"),
    ("Medium-Dark", "1f3fe"),
    ("Dark", "1f3ff"),
]


def collect_emojis(type: str, twemoji: dict[str, str]) -> tuple[set[str], Path]:
    dir = SELF_DIR / "build" / "fluent" / type
    dir.mkdir(parents=True, exist_ok=True)

    out: set[str] = set()
    fluent_assets = SELF_DIR / "fluentui-emoji" / "assets"
    for subdir in os.listdir(fluent_assets):
        with (fluent_assets / subdir / "metadata.json").open(encoding="utf-8") as f:
            meta = json.loads(f.read())
        base_name = subdir
        if meta["cldr"] == "O button (blood type)":
            base_name = meta["cldr"]
        if "unicodeSkintones" in meta:
            for offset, (tone, codepoint) in enumerate(SKINTONES):
                file = (
                    f"{base_name.lower().replace(' ', '_')}_{type}_{tone.lower()}.svg"
                )
                full = fluent_assets / subdir / tone / TYPE_TO_DIR[type] / file
                assert full.exists(), full
                unicode = meta["unicodeSkintones"][offset]
                if codepoint:
                    assert codepoint in unicode
                else:
                    assert unicode == meta["unicode"]  # default
                unicode = unicode.replace(" ", "-")
                if unicode not in twemoji:
                    unicode = unicode.replace("-fe0f", "")
                while unicode.startswith("0"):
                    unicode = unicode[1:]
                dist = dir / f"{unicode}.svg"
                shutil.copyfile(full, dist)
                out.add(unicode)
        else:
            file = f"{base_name.lower().replace(' ', '_')}_{type}.svg"
            full = fluent_assets / subdir / TYPE_TO_DIR[type] / file
            assert full.exists(), full
            unicode = meta["unicode"].replace(" ", "-")
            if unicode not in twemoji:
                unicode = unicode.replace("-fe0f", "")
            while unicode.startswith("0"):
                unicode = unicode[1:]
            dist = dir / f"{unicode}.svg"
            shutil.copyfile(full, dist)
            out.add(unicode)
    return out, dir


def all_twemoji() -> dict[str, str]:
    base = SELF_DIR / "twemoji" / "assets" / "svg"
    return {it.removesuffix(".svg"): str(base.joinpath(it)) for it in os.listdir(base)}


def append_twemoji(existing: set[str], twemoji: dict[str, str], dir: Path):
    for codepoint, path in twemoji.items():
        if codepoint in existing:
            continue
        shutil.copyfile(path, dir / f"{codepoint}.svg")


def main():
    parser = argparse.ArgumentParser(
        "generate-fluent.py", description="Generate a fluentui emoji font"
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
    parser.add_argument(
        "--type", help="Type of fluent emoji", choices=list(TYPE_TO_DIR.keys())
    )
    parser.add_argument(
        "--fallback", help="Use twemoji as fallback", action="store_true"
    )
    args = parser.parse_args()

    twemoji = all_twemoji()
    existing, dir = collect_emojis(args.type, twemoji)
    if args.fallback:
        append_twemoji(existing, twemoji, dir)

    fill_emojis(dir)

    config = make_config(
        output_name=args.output,
        family=args.family,
        color_format=args.color_format,
        paths=[str(dir / it) for it in os.listdir(dir)],
    )
    with tempfile.NamedTemporaryFile("w", suffix=".toml", delete_on_close=False) as f:
        f.write(config)
        f.close()

        subprocess.run(["nanoemoji", f.name], check=True)


if __name__ == "__main__":
    main()
