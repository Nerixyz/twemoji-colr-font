# twemoji-colr-font

This repository contains [Twemoji](https://github.com/jdecked/twemoji) emojis as an OpenType font in different formats using [nanoemoji](https://github.com/googlefonts/nanoemoji).

**The latest builds can be found [here](https://github.com/Nerixyz/twemoji-colr-font/releases)**.

The following formats are available:

- [glyf]
- [glyf] [COLR]v0
- [glyf] [COLR]v1
- [CFF] (v1) [COLR]v0
- [CFF] (v1) [COLR]v1
- [CFF2] [COLR]v0
- [CFF2] [COLR]v1
- Picosvg ([SVG] font)
- Picosvgz ([SVG] font, compressed)
- Untouchedsvg ([SVG] font using original SVG files)
- Untouchedsvgz ([SVG] font using original SVG files, compressed)
- [CBDT] (color bitmaps)
- [sbix] (Safari only - https://github.com/harfbuzz/harfbuzz/issues/2679#issuecomment-1021419864)

[CFF]: https://learn.microsoft.com/en-us/typography/opentype/spec/cff
[CFF2]: https://learn.microsoft.com/en-us/typography/opentype/spec/cff2
[CBDT]: https://learn.microsoft.com/en-us/typography/opentype/spec/cbdt
[COLR]: https://learn.microsoft.com/en-us/typography/opentype/spec/colr
[glyf]: https://learn.microsoft.com/en-us/typography/opentype/spec/glyf
[SVG]: https://learn.microsoft.com/en-us/typography/opentype/spec/svg
[sbix]: https://learn.microsoft.com/en-us/typography/opentype/spec/sbix

You can generate the font locally too (reuqires [uv](docs.astral.sh/uv)):

```sh
git submodule update --init --recursive
uv run generate.py glyf_colr_1 -o font.ttf --family "Twemoji - COLRv1"
```

The font will be located in the `build/` directory.

On Windows, you can use `gen-segoeui.py` to set the name of a font to `Segoe UI Emoji` (copies the name from the default font). This font can then be installed and will get added as a replacement for the default Windows emoji font.

```sh
uv run gen-segoeui.py build/Twemoji_GlyfColr1.ttf -o build/SegoeUI_Twemoji.ttf
```
