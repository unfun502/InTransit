# In Transit

Interactive map of goods on the move, built as a data-viz and mapping demo. The first dataset is modeled European road freight; the name leaves room for rail, sea and air to follow.
Single page, no build step: MapLibre GL for the base map, deck.gl for the data layers.

## Run it

```bash
npm run dev
```

Then open http://127.0.0.1:5186/. The `.claude/launch.json` config named `dev` does the same thing for the in-app preview. Add `?intro=1` to see the first-visit overlay again.

## Deploy

Cloudflare Workers with Static Assets, custom domain intransit.devlab502.net (declared in `wrangler.toml`). `worker.js` adds the fleet security headers and CSP. GitHub Actions deploys on push to main; by hand:

```bash
npm run deploy
```

The share card is `public/og.jpg` (a screenshot of the Decimal continental view, 800×420). Replace it with a 1200×630 render when there is a better one.

## What's in here

| Path | Purpose |
|---|---|
| `index.html` | The whole app: sidebar (Story / Explore / Design), map, layers, tooltips, story chapters |
| `.claude/launch.json` | Preview config: `node server.js 5186` |
| `styles/oil.json` | "Oil Company" base map, a hand-built vintage road-map style on OpenFreeMap vector tiles |
| `styles/moonlight.json` | "Moonlight" base map, minimal dark style on the same tiles |
| `data/*.json` | Prepped subset of the Fraunhofer dataset (see below) |
| `server.js` | Dependency-free static file server for local preview |
| `_dl/` | Raw downloads: the Fraunhofer zip and the FLW map's style JSON. Not needed at runtime |

## Data

Speth, Sauter, Plötz & Signer (2021), *Synthetic European road freight transport flow data based on ETISplus*, Fraunhofer ISI, Mendeley Data, CC BY 4.0.
https://data.mendeley.com/datasets/py2zkrb65h/1

The raw flow file is 2.8 GB (1.5 million region-to-region flows with routed E-road paths). A Python prep script streams it once from the zip and writes:

| File | Contents |
|---|---|
| `nodes.json` | Highway network node id → [lng, lat] |
| `network.json` | Highway edges: [nodeA, nodeB, km, trucks 2019, trucks 2030, manually added] |
| `regions.json` | 1,675 NUTS-3 regions: centroid, country, inbound/outbound tonnes 2019 and 2030, cross-border share, average haul |
| `flows_top.json` | ~3,000 lanes: the biggest by tonnage, the biggest cross-border, and the biggest by tonne-km, each with its routed node path |
| `country_flows.json` | Country-pair totals for the zoomed-out view |
| `region_top.json` | Each region's top 8 destination partners |
| `meta.json` | Row counts and grand totals |

Cost (€) and transit days shown in the app are illustrative estimates layered on top of the data: tonnes × km × a per-country rate, and km ÷ driving speed ÷ hours per day plus border allowances. They are there to show the treatment, not to be quoted.

## Chrome themes

The sidebar, legend, tooltips and chapter plate have two looks, chosen automatically from the base map (`THEME_OF` in `index.html`): a vintage cream "paper" chrome for light bases such as Standard Oil, and a dark "panel" chrome (black, mint phosphor, ember accents, Roboto Condensed and IBM Plex Mono) for Decimal and Midnight. Defaults are Decimal, the Ember flow palette and truck speed 2.

## Base maps and the Mapbox token

Mapbox styles load through MapLibre by rewriting `mapbox://` URLs (see `mapboxTransform` in `index.html`). The page embeds one public token restricted to devlab502.net, which does not work on localhost. For local work, create the git-ignored `public/dev-token.js`:

```js
window.MB_DEV_TOKEN = '<the account's unrestricted default public token>';
```

The page loads that file only on localhost. `?mapbox=<token>` overrides either token.

The Design tab's base-map dropdown also lists Mapbox gallery styles (Standard Oil Company, Mineral, Decimal, Moonlight, Blueprint, American Memory, North Star, Pencil, Frank, Lè Shine, Neon Glow). They load directly from their public style IDs under `mapbox` or `mapbox-map-design`, no cloning into Studio needed; the IDs are in the `BASEMAPS` table in `index.html`. Gallery pages have removed the add-to-Studio button for several of these, but the styles remain publicly readable. Only classic (v8) styles work here; Mapbox Standard-based styles (the "Default", "Faded", "Monochrome" templates) will not render in MapLibre.

Three keyless base maps need no token: "Oil Company" and "Midnight" are hand-built styles in `styles/` on OpenFreeMap tiles, "Positron" is OpenFreeMap's own.
