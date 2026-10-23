# tnballers.com

Live site: https://tnballers.com (Netlify project "tnballers", publishes the `site/` folder on every push to `main`).

## Layout
- `site/index.html`: the published site. Generated. Never edit by hand.
- `src/`: everything the site is built from.
  - `src/parts/nine_data.js`: the 8 TNB partner players (stats per competition in `comps`, `STATS_ASOF` date at the top, highlights, sources).
  - `src/parts/feed.json`: the Live Tracker feed (newest items show on the homepage; all on the Canada tab). Add one item per real event: {"date":"YYYY-MM-DD","tag":"TNB|Goal|Trophy|Award|Injury|Transfer|Call-up|Matchday","headline":"short","detail":"one or two sentences with the facts","link":"source URL"}. Keep the newest ~30; drop older ones.
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
- Post templates (fixed TNB designs, not AI-generated) are in `site/templates/` (goal, matchday, ranking, news), published at https://tnballers.com/templates/<name>.html. Their master copies are imported into Canva; the Canva design IDs are listed below once created.
- To make a post: copy the matching master design in Canva (copy-design), open it with read-design (open_transaction: true), replace the text elements (replace_text / find_and_replace_text) with today's facts, swap the photo element (update_fill) with an uploaded photo asset, commit, then export as PNG. Never use Canva's AI generators for posts.
- Partner player cut-outs (transparent PNG, real headshots supplied by TNB): https://tnballers.com/players/<key>.png for bibishkov, ciccarelli, tavernier, bruno, olguin, keshavarz, greco-taylor, pavela. Upload with upload-asset-from-url.
- Other players: real photos found online, uploaded to Canva with upload-asset-from-url (prefer the player's own posts, official club posts, Wikimedia Commons, or a named photographer). Put the credit in the caption and in the "PHOTO CREDIT" line ("📸 @photographer / @club"). Never use photos watermarked by agencies (Getty, Imago, Shutterstock, AP, Reuters, PA, etc.). Record every photo's source in the report.
- Look: black background, red diagonal stripe, gold accents, white condensed uppercase type (Bebas Neue / Barlow Condensed), maple leaf accent, "@tnballers" footer.

## Canva master templates
Copy these (never edit the masters themselves):
- Goal / big moment: DAHY1r2A_UA. Elements: headline "GOAL.", player name, red match line, grey detail line, red badge (text inside a shape: use find_and_replace_text on the shape), photo slot (shape with image fill: update_fill), "📸 PHOTO CREDIT" line.
- Matchday: DAHY1goGMmQ
- Canada's Best ranking (5 rows, no photo): DAHY1hX-TJs
- News / trophy / transfer: DAHY1v1jl9Y
- Example finished post: "TNB Post – Davies scores vs Arsenal (21 Oct 2026)", DAHY15t_Y8I.
Workflow: copy-design → read-design (open_transaction: true, fields design_content) to get locator_ids → edit-design keep_open with replace_text / find_and_replace_text / update_fill / format_text / update_title → check the returned thumbnail → edit-design commit → export-design PNG 1080x1350. Title copies "TNB Post – <what> (<date>)".
Text colour gotcha: the grey detail line imports as black; set format_text color #E6E6E6 when you replace it.

## Photo sources that work with Canva upload-asset-from-url
- Partner players: https://tnballers.com/players/<key>.png (best quality).
- Bundesliga players: the official cut-out from the bundesliga.com player page, e.g. https://assets.bundesliga.com/player/<id>-body.png (find the URL in the page's og:image:secure_url; drop the query string). Credit "📸 BUNDESLIGA / @CLUB".
- Club and league sites often block Canva's downloader (fcbayern.com did). FotMob images are only 192px: avoid unless nothing else exists.
