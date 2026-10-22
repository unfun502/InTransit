# CLAUDE.md — In Transit

## What this app does
Interactive map of goods on the move, built as a data-viz and mapping demo for prospective clients. First dataset: 1.5 million modeled European road-freight flows (Fraunhofer ISI, ETISplus-based, CC BY 4.0), routed over the E-road network, with 2010/2019/2030 tonnage and trucks. Features: story chapters with fly-tos and on-map callouts, routed / arc / animated-convoy flow rendering, highway load, region hubs with top partners, year and measure switches, illustrative cost and transit-time estimates, and a dozen switchable base maps with two chrome themes.

## Tech stack
Plain HTML/CSS/JS, single file (`public/index.html`), no build step. MapLibre GL 4 (cdnjs) for the base map, deck.gl 9 (unpkg) for data layers. Google Fonts. Cloudflare Workers with Static Assets.

## Domain
intransit.devlab502.net (custom domain on Workers, declared in `wrangler.toml`)

## Build & deploy
- No build step. `worker.js` serves `public/` through the `ASSETS` binding with security headers (`run_worker_first = true`, `not_found_handling = "none"`).
- Deploys via GitHub Actions → `wrangler deploy` on push to main (`.github/workflows/deploy.yml`), or by hand with `npm run deploy`.
- Local preview: `npm run dev` (dependency-free static server on port 5186), or the `dev` entry in `.claude/launch.json`.

## Base maps and tokens
- `public/index.html` embeds one public Mapbox token, URL-restricted to devlab502.net (1Password: "Mapbox public token — devlab502 (all apps)"). It does not work on localhost. For local work create the git-ignored `public/dev-token.js` with `window.MB_DEV_TOKEN = '<unrestricted default token>'` (1Password: "Mapbox public token (default)"); the page loads that file only on localhost. `?mapbox=<token>` overrides either. Never commit the unrestricted token: GitHub push protection flags Mapbox tokens, and the restricted one has been allowed once as a false positive.
- Mapbox gallery styles load directly by public style ID (table `BASEMAPS` in `index.html`); only classic v8 styles render in MapLibre, Mapbox Standard-based ones do not.
- Keyless fallbacks in `public/styles/` run on OpenFreeMap tiles.

## Data
`public/data/*.json` is a prepped subset of the 2.8 GB Fraunhofer flow file plus NUTS-3 polygons (GISCO), Eurostat commodity mix, per-segment corridor profiles and the maritime layer (Eurostat port tonnage by partner sea area, routed with `searoute`). See README for each file and the scripts in `scripts/`. Raw downloads live in `_dl/` (git-ignored). Cost (€) and transit days, road and sea, are illustrative formulas, not data.

## Environment variables
None required. Optional Worker var `UMAMI_SITE_ID` enables analytics injection.

## Contact
devlab502@proton.me
