# RSL GFX Studio — source

Web app that makes Roshn Saudi League graphics (EN + AR) from live data, exported as 2160px-wide JPGs.

See PROJECTS.md for the design projects in `projects/`.

## Layout
- `studio/index.html` — the whole app (single file, canvas drawing in PSD pixel coordinates).
  Key functions: drawTable, drawMW, drawDay, drawFT, drawThumb, drawGS, drawShort, drawCmp, drawAch, nineSlice, autoCutout. Templates: TEMPLATES / GROUPS.
- `studio/assets/` — template art, photos, logos, fonts (Lama Sans, Expanded Numbers). Bump `ASSET_V` in index.html whenever any art changes.
- `site/build.sh` — builds the password-protected team website (website mode, `rsl-pass` = SHA-256 of the password).
- `site/league.sample.json` — sample of the data file the site reads from `data/league.json`.
- `tools/psdlayers.py` — PSD layer / text parser used to match templates to the PSDs.

## Where things live
- Team website: https://rsl-gfx.github.io (repo RSL-GFX/rsl-gfx.github.io, serves the built `site/dist`).
- Admin + database: the Claude artifact (slug eecf3a6a-299c-4e13-955d-4af843b65fff); collections teams/*, mws/mw01..34, league/settings, league/official, league/sync, league/scorers.
- Data: fixtures/results/table from saff.com.sa, scorers from spl.com.sa (scheduled sync tasks), published to data/league.json.

## Publish
1. `PASS_HASH=... ./site/build.sh`
2. Copy `site/dist/*` into the rsl-gfx.github.io repo, commit, push to main.

## Rules
- Arabic is mirrored (home on the right), titles upright, Expanded Numbers upright; use الجولة not MW.
- Uploaded photos reset on refresh (no localStorage).
