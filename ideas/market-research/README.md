# Market Research — fidget-tier opportunity

A monochrome, tab-by-tab market read for a fidget-spinner-tier product,
presented in the **minimono-glass** house style (pure black/grey/white, big
type, one Liquid Glass tab bar, no accent color, responsive phone→desktop).

Four tabs: **Markets** (sizing + TAM/SAM/SOM) · **Rivals** (handheld-calm
competitors and their prices) · **Trends** (the 2026 tailwinds) · **Verdict**
(the synthesis + sources).

## Files
- `market.html` — the built, self-contained page (published as an Artifact).
- `market.src.html` — the source with `/*__LG_CSS__*/` and `/*__LG_JS__*/`
  markers, before the Liquid Glass assets are inlined.

## Rebuild
The Artifact sandbox blocks external assets, so the glass CSS/JS are inlined.
To rebuild after editing `market.src.html`:

```bash
python3 - <<'PY'
import pathlib
base="/root/.claude/skills/synced/minimono-glass/glass/assets"
src=pathlib.Path("market.src.html").read_text()
css=pathlib.Path(base+"/liquid-glass.css").read_text()
js =pathlib.Path(base+"/liquid-glass.js").read_text()
pathlib.Path("market.html").write_text(
    src.replace("/*__LG_CSS__*/",css).replace("/*__LG_JS__*/",js))
PY
```

## Data
Figures are from an Aug 2026 research pass; sources are listed on the
Verdict tab. Syndicated market sizes vary 2–5× by firm — the page shows the
most-cited value with the range footnoted.
