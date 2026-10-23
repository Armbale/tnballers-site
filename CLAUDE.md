# tnballers.com

Live site: https://tnballers.com (Netlify project "tnballers", publishes the `site/` folder on every push to `main`).

## Layout
- `site/index.html`: the published site. Generated. Never edit by hand.
- `src/`: everything the site is built from.
  - `src/parts/nine_data.js`: the 8 TNB partner players (stats per competition in `comps`, `STATS_ASOF` date at the top, highlights, sources).
  - `src/parts/make_canada.py`: "Canada's best right now" (`BEST`), the sidelined list (`SIDE`), and the legends section (`NOW`, `HOME`, `MOMENTS`). Also update the "as of" date in the `can-note` text.
  - other `src/parts/*`: page sections, styles and scripts.
- `src/build.sh`: rebuilds `site/index.html`. Must finish with "Built ../site/index.html".

## Updating stats
1. Edit only the data in `src/parts/nine_data.js` and/or `src/parts/make_canada.py`.
2. Update `STATS_ASOF` (and the as-of text in `nine_table.html` / `make_canada.py`) to today's date, e.g. "18 Oct 2026".
3. Run `src/build.sh`. If it fails, fix or revert; never push a failed build.
4. Sanity checks before committing: season totals never go down; minutes <= 90 x apps (+ extra time); a player can't gain more goals than games played that day would allow. If a number looks wrong or can't be confirmed from two sources, leave the old value and say so in the report.
5. Commit `src/` and `site/` together with a message like "Stats update 18 Oct 2026: Olguin +1 app, ..." and push to `main`. Netlify goes live in about a minute.

## Rules
- Stats source: FotMob player pages (IDs are in the data files). Cross-check goals, injuries and transfers with a second source.
- Do not reveal individual market values or their sources.
- Keep Canadian/British spelling.

## Social content (Instagram)
- Player cut-outs (transparent PNG, real headshots supplied by TNB) are published at https://tnballers.com/players/<key>.png for: bibishkov, ciccarelli, tavernier, bruno, olguin, keshavarz, greco-taylor, pavela. Use them in Canva via upload-asset-from-url.
- Other photos found online: prefer the player's own posts, official club posts, or a named photographer who can be tagged. Always credit in the caption ("📸 @photographer / @club"). Never use photos watermarked by agencies (Getty, Imago, Shutterstock, AP, Reuters, etc.). Note every photo's source in the briefing.
- Look: black background, red diagonal stripe, gold accents, white condensed uppercase type, maple leaf accent, "@tnballers" footer, matching the site.
