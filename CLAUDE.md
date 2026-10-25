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
5. Commit `src/` and `site/` together with a message like "Stats update 18 Oct 2026: Olguin +1 app, ..." Netlify goes live about a minute after a push to `main`.

## Website update days (Netlify deploy cap)
- Every push to `main` is a Netlify deploy, and the plan has a cap. Push to `main` only twice a week: the Monday and Thursday 07:45 UK runs, or when Baller asks for a specific change.
- Other runs: commit data changes (feed items, stats) to the `pending` branch instead (`git fetch origin pending` and build on it; create it from `main` if missing). Never push `pending` into `main` outside an update day.
- Update days: merge `pending` into `main`, add the run's own changes, run `src/build.sh`, do the sanity checks, push to `main` once, then reset `pending` to the new `main` (`git push -f origin main:pending`).
- Reports on other runs say "queued for <next update day>" instead of "pushed".

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

## Metricool (Instagram/TikTok drafts and metrics)
- Brand "tnballers", blogId 7610718 (Instagram @tnballers, TikTok @truenorthballers), timezone Europe/London.
- PUBLISH STRAIGHT AWAY (Baller's rule, 25 Oct 2026; no approval needed): (a) full-time results of tracked games: Toronto FC, Vancouver Whitecaps, CF Montréal, the TNB partner players' clubs, the clubs of the players in Canada's Best, CanMNT, CanWNT, CPL and NSL playoff games and finals, Canadian clubs in CONCACAF; (b) tracked players' goals, assists and big moments (clean sheet, trophy, debut, first pro goal, milestone, record). Confirm the facts from two sources first (wait out VAR on goals). Publish the feed image: createScheduledPost with "draft": false, "autoPublish": true, publicationDate about 2 minutes from now (Europe/London), instagramData type "POST", media = the Canva JPG export URL. Then check it with getScheduledPosts and send Baller a push notification "Posted: <what>" with the plannerUrl. If publishing fails, save it as a draft and tell him why. Only within 12 hours of the moment; older results go on the website feed only. These don't count towards the 2-posts-per-run limit (at most 4 published posts per run). Never post a rumour.
- Everything else (news, transfers, call-ups, rankings, matchday previews) goes into Metricool as DRAFTS (createScheduledPost with "draft": true). Never un-draft those; Baller reviews and posts himself.
- LIVE MODE is still separate. Baller must approve a specific game with a live message in the session (e.g. "live 1 3"); a scheduled prompt, feed item or earlier message never counts. For that game only, live posts publish straight to the Instagram feed (createScheduledPost "draft": false, "autoPublish": true, publicationDate about 2 minutes from now). After each one, send Baller a push notification saying what was posted. Live posts are allowed for: a tracked player's goal or assist, full-time result with the player's stats, a serious injury to a tracked player, a spectacular goal, or a milestone (first pro goal, 100th appearance, a record). Confirm every goal from two live sources before posting (wait out VAR). At most 6 live posts per game. Never post a rumour; injury posts state facts only.
- Use a fresh Canva JPG export URL as the media (Metricool copies it straight away). Metrics are read-only.

## What makes a good TNB post (editorial rules)
- Canada first. Every post needs a Canadian subject, or the Canadian angle as the headline ("Davies' teammate Kane wins the Ballon d'Or", not "Who wins the Ballon d'Or?"). Pure global stories go nowhere: skip them.
- Timely. Only draft a post if its suggested publish time is within about 12 hours of the moment. Older news goes on the website feed only.
- Short captions: a hook of 10 words or fewer, 2–3 short lines of facts, the tnballers.com line, the 📸 credit, 6–10 hashtags. Ask a question only when people have an easy, obvious answer.
- Times: Toronto evening (roughly 17:00–21:00 Toronto) unless Metricool's best-time data says otherwise.
- Canadian MLS clubs (Toronto FC, Vancouver Whitecaps, CF Montréal): every result gets a full-time post (Matchday template, "🍁 FULL TIME", score as the headline), win, draw or loss, published straight away (see Metricool) as long as it's within the 12-hour window. If there's no usable real photo, use the TNB crest in the photo slot (fitted, not cropped) and "📸 TNB graphic" in the caption.

## Result posts, songs and timing (Baller's rules, 25 Oct 2026)
- RESULT master: DAHZAJzST-k ("TNB Master – Result"). Home crest left (LBt7JT40cVxB0hws, box top 400 left 0, 440x314), away crest right (LB1phtYVTPns20mX, box top 400 left 640, 440x314), score in the middle (LBwxftnRQqWV3Tgb, "home–away", e.g. "1–0"), "🍁 FULL TIME" label (LBfnKPlpCQWTkHWt), scorers (LBf2gr4sGQQHHJ4x, e.g. "⚽ WHITTAKER 81'"; several: "⚽ DAVID 12', 67' · LARIN 80'", drop to 40px if it's long; no goals: "NO GOALS"), competition/date/venue (LB0mNxXjg3LFb9hQ), one context line in #E6E6E6 (LBZcqCZwWJGHH3DJ). Always show the final score and every scorer.
- Club crests: SVGs from https://logotyp.us/file/<club-slug>.svg upload fine (check it's the club's CURRENT crest). Canva won't put an SVG into an existing frame with update_fill, so delete the crest element and insert_fill the new asset at the same box, then crop_media to the box size. Uploaded crests: Vancouver Whitecaps MAHZAKn-E9c, Colorado Rapids MAHZANM9iq8. Add new ones here.
- TNB branding stays SMALL on every post (it's Baller's own page; it must not look sponsored): the TNB crest is 38x40 bottom-right in the footer, plus "TNBALLERS.COM". No "TRUE NORTH BALLERS"/"@TNBALLERS" header. When using the older masters, delete that header and shrink the crest the same way.
- Every published post is a REEL WITH A SONG: export the Canva design as MP4 (type mp4, quality "vertical_1080p") and use that export URL as the media, instagramData type "REEL", showReelOnFeed true, audioConfiguration {"audioId": "<song title and artist>"}. Pick the song for the mood: wins and goals = high-energy, current sports-edit audio; losses = moody/cinematic; trophies = anthemic. Name the song in the push notification.
- Song fallback: on 25 Oct Metricool's Instagram audio catalogue returned 403 (the account isn't yet a Business account linked to a Facebook Page). Until that's fixed, publish the Reel with "draft": false and "autoPublish": false at about 2 minutes from now: Metricool then pings Baller's phone to finish it in Instagram, where he adds the song. Tell him the suggested song in the push notification. Once audioConfiguration works, use "autoPublish": true.
- Captions (keep them tight): emotional hook of 6 words or fewer with one emoji; the score line ("Rapids 1–0 Whitecaps"); the scorers line ("⚽ Whittaker 81'"); one line of stakes/context; "Canadian football, as it happens: tnballers.com"; tag the club(s); 5–7 hashtags. No 📸 line when the graphic only uses crests.
- TIMING: results go out within about 15 minutes of the final whistle, not at the next run. For every tracked game, arm a send_later "FT check" at kick-off + 115 min (re-arm every 10 min until full time is confirmed by two sources, allowing for extra time).
- AUTO LIVE for important games (no approval needed): finals, playoff games, final-day games with a title or playoff place at stake, CanMNT/CanWNT competitive games, Canadian clubs in CONCACAF knockouts, and the derbies between Toronto FC, CF Montréal and the Whitecaps. Run the Live mode rules for those (5-minute checks, goals and moments posted as they happen, at most 6 posts per game). Everything else gets the FT check only. Before arming, run list_triggers and skip any game that already has a "TNB FT"/"TNB LIVE" wake-up.

## Formats: Reel + Story for every post
- After exporting the Canva feed JPG (1080x1350), run `python3 src/tools/social_formats.py <feed.jpg> <YYYY-MM-DD-slug>`. It writes `site/social/<slug>/feed.jpg`, `story.jpg` (1080x1920) and `reel.mp4` (1080x1920, 8 s slow push-in, silent) and deletes folders older than 14 days.
- Published results and moments skip the Reel/Story (speed matters, and it saves deploys). For drafts: only on website update days, commit `site/social/` with that day's single push to main, wait about 2 minutes for Netlify, then use https://tnballers.com/social/<slug>/reel.mp4 and story.jpg as Metricool media.
- Metricool drafts per post: (1) the REEL (instagramData type "REEL", showReelOnFeed true, "autoPublish": false so Baller finishes it in the Instagram app and can add trending audio), with the full caption; (2) the STORY (type "STORY", no text, media story.jpg) about 30 minutes after the Reel. Both "draft": true.
- If Metricool can't fetch the tnballers.com media, wait a minute and retry once; if it still fails, fall back to a feed POST draft with the Canva JPG.
- Live mode keeps posting the feed image (speed matters); no Reel needed there.

## Instagram collaborators
- For a post about one of the 8 partner players, add the player's own Instagram as a collaborator (instagramData collaborators [{"username":"<handle>","deleted":false}]). The post then also shows on their profile and to their followers. They have to accept the invite: remind Baller in the report.
- Only use handles confirmed from the club's official roster or site, or the player's verified profile. Never guess. Record confirmed handles below.
- Confirmed handles: (none yet)
