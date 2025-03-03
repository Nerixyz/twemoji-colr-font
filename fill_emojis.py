import os
from pathlib import Path
import json
import regex
import shutil

Codepoint = tuple[int, ...]


def fill_emojis(dir: Path):
    unified_to_unqual, unqual_to_unified = _load_emoji()

    files = {_from_filename(f): f for f in os.listdir(dir)}

    for codepoint, file in files.items():
        if codepoint in unified_to_unqual:
            uq = unified_to_unqual[codepoint]
            if uq is None:
                continue
            if uq in files:
                continue  # already present
            shutil.copyfile(dir / file, dir / f"{_string(uq)}.svg")
            # print(f"Filling in {_string(uq)}")
        elif codepoint in unqual_to_unified:
            q = unqual_to_unified[codepoint]
            if q in files:
                continue  # already present
            shutil.copyfile(dir / file, dir / f"{_string(q)}.svg")
            # print(f"Filling in {_string(q)}")
        else:
            print(f"Missing {_string(codepoint)}")
    print("filled missing")


def _from_filename(filename: str) -> Codepoint:
    match = regex.search(r"(?:^emoji_u)?(?:[-_]?([0-9a-fA-F]{1,}))+", filename)
    if not match:
        raise ValueError(f"Bad filename {filename}; unable to extract codepoints")
    return tuple(int(s, 16) for s in match.captures(1))


def _string(codepoints: Codepoint) -> str:
    return "_".join("%04x" % c for c in codepoints)


def _load_emoji():
    with (Path(__file__).parent / "emoji.json").open() as f:
        content = f.read()
    emojis = json.loads(content)
    unified_to_unqual: dict[Codepoint, Codepoint | None] = dict()
    unqual_to_unified: dict[Codepoint, Codepoint] = dict()

    def push_emoji(emoji):
        nonlocal unified_to_unqual
        nonlocal unqual_to_unified
        nq = emoji["non_qualified"]
        has_nq = nq is not None
        if has_nq:
            nq = _from_filename(nq)
        u = _from_filename(emoji["unified"])
        unified_to_unqual[u] = nq
        if has_nq:
            unqual_to_unified[nq] = u

    for emoji in emojis:
        push_emoji(emoji)
        if "skin_variations" in emoji:
            for v in emoji["skin_variations"].values():
                push_emoji(v)
    return unified_to_unqual, unqual_to_unified
