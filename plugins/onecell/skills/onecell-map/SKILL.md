---
name: onecell-map
description: >
  Put an interactive map on a onecell page from an analysis, a dataset or a collection.
  First choice is the core onecell.map block type: pins, uploaded GeoJSON or live
  collection layers as points, lines, areas or a heatmap, coloured by field or a ramp,
  with popups, a legend and saved views, written as data. Falls back to a hand-built
  MapLibre sandbox block only for what the type can't do. Trigger when the user wants a
  map on a onecell page, wants to turn a dataset, analysis output or collection into a
  onecell map, or wants an existing onecell map (type or sandbox) upgraded, fixed or
  extended.
---

# onecell map

Put a map on a onecell page that people can pan, zoom, toggle and click. Write it as an
`onecell.map` block (data only, drawn by onecell's reviewed renderer, searchable as
text) unless it needs something the type can't do; then build a sandbox. Written from
maps that worked (and broke) in real use: coverage gaps, a site library, and cards of
candidate sites.

Companion to `https://onecell.io/skills/onecell.md`; read it first if it isn't loaded this session.
This skill assumes its write rules (dry runs, `expected_version`, drafts, decision
points). Re-fetch this file from `https://onecell.io/skills/onecell-map.md` once per session, with
the others. Check the live version and fields with `list_block_types name: "onecell.map"`:
the notes below are for `onecell.map@5`, and a newer version wins.

Files that come with this skill, next to it in the plugin or at these addresses:
- `scripts/to_geojson.py`: `https://onecell.io/skills/onecell-map/scripts/to_geojson.py`
- `assets/map-template.html`: `https://onecell.io/skills/onecell-map/assets/map-template.html`

## 1. Shape the data

- **Aggregate only.** A layer reaches every reader of the page. No personal data, no
  per-person points; ZIP-, site- or venue-level aggregates only. Check the project's
  privacy rules before uploading.
- **Fewer than about 200 places with a name and a note?** Use the block's own `pins`;
  no upload needed.
- **More, or shapes (areas, lines), or numbers to colour by:** one GeoJSON file per
  layer, a FeatureCollection with the properties the popups, colours and sizes need.
  Keep property names short.
- `scripts/to_geojson.py` (see above) turns a CSV with lat/lng columns into a layer file: `python to_geojson.py sites.csv sites.geojson --props name,households`. Only the columns you name leave the machine.

## 2. Upload the layers

- `create_upload` with `document_id` = the page the map goes on, `kind: "file"`,
  filename ending `.geojson`, `dry_run: false`; then
  `curl -sS -X PUT --data-binary @file '<upload_url>'`. The link is single-use and lasts
  10 minutes: create it right before the PUT. Keep the returned `asset.id`.
- **Collections:** a layer `{name, collection: '<collection block id>'}` for one on the
  same page, adding `document: '<document id>'` for one on another page **in the same
  cell** (never another cell). Items with a location field arrive as live GeoJSON points
  (properties: `key`, `title`, `status`, `statusLabel` and every field), for signed-in
  readers only: on a public page a collection layer is missing, so upload a snapshot too
  if the map will be public.
- Up to 10 layers per block.

## 3. Write the block (first choice)

```json
{
  "type": "custom",
  "kind": "onecell.map@5",
  "layers": [
    { "name": "zips", "assetId": "<uploaded .geojson asset id>" },
    { "name": "sites", "collection": "<collection block id>", "document": "<its page, if another>" }
  ],
  "data": {
    "title": "Distance from each area to the nearest venue",
    "caption": "One line on the source and date",
    "size": "Large",
    "styles": [
      { "layer": "zips", "label": "Distance to the nearest venue", "kind": "Areas",
        "colour": "Ramp by field", "colour_field": "nearest_venue_mi",
        "ramp_breaks": "2.5, 5, 7.5, 10", "ramp_hue": "Blue", "ramp_direction": "Low is dark",
        "colour_labels": "Under 2.5 mi, 2.5–5 mi, 5–7.5 mi, 7.5–10 mi, 10 mi or more",
        "fill_opacity": 0.7, "title_field": "place",
        "popup_fields": "households:Households, nearest_venue_mi:Miles to nearest venue" },
      { "layer": "sites", "label": "Sites to vet", "kind": "Points", "colour": "By status",
        "title_field": "title" }
    ],
    "views": [ { "name": "Niagara County", "sw": { "lat": 42.99, "lng": -79.09 }, "ne": { "lat": 43.38, "lng": -78.45 } } ]
  }
}
```

- **One `styles` row per layer**, its `layer` matching the layer's `name`. A layer with no
  row is drawn as default points; a row whose layer didn't arrive (a typo, an unreadable
  file, a collection on another cell's page) is named in a note under the map.
- **`kind`:** Points, Lines, Areas or Heat (`weight_field`, `heat_radius`).
- **`colour`:** a fixed colour (Blue, Green, Orange, Red, Purple, Teal, Grey); `By status`
  for a collection (its own tones); `By field` (categories of `colour_field`, named with
  `colour_labels: "1:Yes, 0:No"`); `Ramp by field` for a choropleth (`colour_field`
  numeric, `ramp_breaks` as class edges or empty for five equal classes, `ramp_hue`,
  `ramp_direction`, and `colour_labels` one per class).
- **Points:** `size_field` sizes dots by a number, `dot_size`, `label_field` labels them.
- **Popups:** `title_field`, and `popup_fields` as `key:Label, key:Label`.
- **Pick one out:** `highlight_field` + `highlight_value` (+ `highlight_label` for the
  legend), e.g. the site being discussed.
- **`views`:** named zoom buttons, each a south-west and north-east corner. **`center` +
  `zoom`** set the opening view; without them it opens on the first view, or fits the
  data when there are no views.
- **`pins`:** `{name, where: {lat, lng}, note?, group?}`, up to 200.
- Never send `text`: the server writes it from `data`. The server checks `data` against
  the version and refuses with each problem's path; fix and retry.
- Escaping, theme, basemap, the legend and missing layers are the renderer's job. The
  map follows the reader's light or dark theme, live.

## 4. Test on a private draft first

1. `create_document` in Inbox (or a scratch draft in the target cell, so a collection
   layer with `document` can resolve): a page with just the map block and its `layers`.
   Asset layers may point at assets uploaded to another of your pages.
2. Open it in Chrome (claude-in-chrome) and screenshot. In the app a type's renderer
   runs as the page opens; on public and share pages it waits behind Run. The frame runs
   on its own domain: check by screenshots and clicks (popups, views, zoom), not its DOM.
3. Check light and dark, and a phone width (a 390px iframe on the page, as the window
   can't shrink that far).
4. A layer that doesn't show: read the note under the map, which names any styled layer
   that didn't arrive. Is the `styles.layer` spelled as the layer `name`? Is the
   collection on a page in the same cell? Are you signed in (collections)?

## 5. Put it on the page

- `update_document` `block_ops`: `replace` the existing block by id (it keeps its id), or
  `insert` with `before`/`after`, with `expected_version`, **dry run first**, then apply.
  Update the text that explains the map in the same call.
- To change the map later, replace the block's `data` (and `layers`); nothing else.
- Re-open the real page in Chrome and check it again.
- Offer to trash the scratch drafts (restorable 30 days); don't trash unasked.

## 6. When the type can't do it: a sandbox block

Use a hand-built `sandbox` block only for what `onecell.map` doesn't draw: values
computed in the page from a compact dataset (sliders, recalculated catchments), custom
tabs or controls, animation, or overlays beyond points, lines, areas and heat. Say why in
the block's `description`. Start from `assets/map-template.html` (see above); it already
follows these rules:

- **Libraries by relative path only:** `/sandbox/vendor/maplibre-gl@5.24.0/maplibre-gl.js`
  and `.css` (also `/sandbox/vendor/d3@7.9.0/d3.min.js`). No CDN, no other network.
- **Basemap:** `/sandbox/maps/style/light.json` or `dark.json`, from
  `data-onecell-theme` on `<html>`; observe that attribute (a `MutationObserver`) and
  `map.setStyle(url, { diff: false })` when it changes. Don't hard-code its font names:
  read a `text-font` from `map.getStyle().layers` for any text labels.
- **Data:** `window.onecell.layers.<name>` is a short-lived URL per reader. Pass it as a
  geojson source's `data`, or `fetch` it for computed data (a compact JSON object can
  ride in a FeatureCollection as a foreign member: `{"type":"FeatureCollection",
  "features":[],"mydata":{...}}`). Check it exists and show a visible note when it
  doesn't. Never put a link or data URL in the HTML.
- **Add sources and layers in `style.load`**, which fires again after `setStyle`.
- **Never set `filter: null`.** MapLibre rejects it and drops the layer silently: omit the
  key. Use `map.on('error', ...)` to surface style errors in the page.
- **Escape every value in popup HTML** (`esc()`), numbers included: collection fields are
  typed by people.
- Colours as CSS tokens on `:root` and `:root[data-onecell-theme="dark"]`.
- Limits: 256 KB of HTML per block, 3 sandboxes per document, `description` required to
  publish, `height` 80-2000. Test it as in step 4, but a sandbox someone else wrote waits
  for **Run** in the app too.

A standalone HTML file (outside onecell) can't load the vendor paths or basemap: keep a
separate template for it if one is needed.

**Upgrading an old sandbox map:** if everything it shows fits the type (pins, styled
layers, popups, views), replace the sandbox block with an `onecell.map` block using the
same `layers`, check it as in step 4, and keep the sandbox only if something is lost.
