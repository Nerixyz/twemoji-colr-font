from fontTools.ttLib import TTFont
import argparse
import os
import shutil


def main():
    semj_path = f"{os.environ['SYSTEMROOT']}/Fonts/seguiemj.ttf"
    parser = argparse.ArgumentParser(
        "gen-segoeui.py", description="Generate a font with the segoeui name"
    )
    parser.add_argument(
        "-o", "--output", help="Output file name (e.g. font.ttf)", default=semj_path
    )
    parser.add_argument(
        "input",
        help="The font to apply the name to",
    )
    args = parser.parse_args()
    og = TTFont(semj_path)
    target = TTFont(args.input)
    # shutil.copyfile(semj_path, semj_path + ".bak")

    target["name"] = og["name"]
    target.save(args.output)


if __name__ == "__main__":
    main()
