# Roma Norte Building by Building

Working repository for Brian Gross's book cataloguing the historic buildings of Colonia Roma Norte, Mexico City (one page per building, churches excluded).

## Build

Run from the repo root (needs Python 3 with pypdf, reportlab, Pillow; Node with Playwright/Chromium):

```
python3 build/gen4.py              # data -> out/book.html
python3 build/shrink_assemble.py   # -> out/Roma Norte Building by Building.pdf
```

`shrink_assemble.py` downsizes images, renders the body with Chromium (Letter), then merges front matter (pp. 1–9) and appendix (pp. 320–329) from `sources/draft3.pdf` and renumbers the appendix. Pass an output path as the first argument to write elsewhere.

## Layout

| Path | What |
|---|---|
| `build/` | Generator (`gen4.py`), PDF assembly, page CSS (`page.html`), hand-made fragments for Puebla 112 / Puebla 109 |
| `data/pages_struct.json` | Per-building fields parsed from draft 3 (location, built, architect, style, uses, notes, sources) |
| `data/titles_v5.json` | Order, address, title line (with tenant), current-use text |
| `data/gm_use.json` | Businesses Google Maps lists at each address (Oct–Nov 2026) |
| `data/denue_matches.json` | INEGI DENUE business directory matches (May 2026) |
| `data/streetview/` | One verified Street View screenshot per entry (`RN-xxx.jpg`, `Dxx.jpg` for demolished sites); `meta/` holds panorama ids, the label each shot shows, and the verification log |
| `data/tavares/` | English translations of Tavares, *Colonia Roma* (Clío), per building, with Kindle locations; `demolished/` for lost buildings |
| `data/research/` | Raw tenant research and geocodes |
| `sources/` | Draft 3 PDF; OCR of the Tavares Kindle screenshots (private research use only) |
| `photos/` | Commons photos from draft 3 (`d3/`) and Brian's own photos (`user/`) |

IDs: `RN-001`…`RN-289` = buildings (draft-3 numbering), `P109` = Puebla 109 conjunto, `D01`…`D14` = demolished sites.
