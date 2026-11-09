---
name: onecell-cards-collection
description: >
  Turn a list of things that each have a picture (sites with satellite crops,
  products, venues, designs) into a onecell collection block: one card per item
  with its image, fields, a location and a status people set as they vet them.
  Covers the field schema, uploading the images, keyed upserts in batches,
  refreshing later without losing verdicts, reading the team's comments back, and
  the gotchas. Trigger when the user wants cards, a board or a vetting list in
  onecell from a CSV, a folder of images or an analysis output, or wants an
  existing collection refreshed or its verdicts read.
---

# Cards in a onecell collection

Written from a real vetting list of 178 candidate sites, each with a satellite crop,
that a team worked through card by card.

Companion to `https://onecell.io/skills/onecell.md`; read it first if it isn't loaded this
session. Its write rules (dry runs, drafts, decision points) apply. Re-fetch this file
from `https://onecell.io/skills/onecell-cards-collection.md` once per session, with the others.

Comes with `scripts/build_items.py`, next to this file in the plugin or at
`https://onecell.io/skills/onecell-cards-collection/scripts/build_items.py`.

## 1. Make the index and the images

One CSV row per item, with:
- a **stable key** you can rebuild on every run (`CO-1`, `X-<source id>`, a hash of
  rounded coordinates for things with no id). The key is how a re-run finds the item
  again. It is set when the item is created and never renamed;
- the fields the card shows and people filter by, with short column names;
- `lat`/`lng` if the item has a place (gives a location field, and lets a map show
  the items);
- the image file name.

Images: untitled (the card shows the title), **16:10** (cards crop to that shape; the
full image shows when an item is opened), JPEG about 80% quality, under 8 MB each.
Keep anything licensed (satellite imagery) inside the team: in a team cell, out of git,
never on a public page.

## 2. Define the block

A `collection` block (see `https://onecell.io/skills/onecell/reference/blocks.md`):
- `fields`: `{key, type, label}`, at most 24; types text, number (`unit` optional),
  select and multi (`options`), date, url, image, location;
- `card`: `{image, title, subtitle, metrics: [...]}` naming field keys, up to three
  metrics; `title` is a text field;
- `status`: `{label, options: [{key, tone, label}]}`, at most 12, e.g. todo/neutral,
  good/success, recheck/warning, drop/danger. New items start on the first;
- `source: {kind: "items"}`, a `title` and a `description` (needed to publish).

Put it on the page with `update_document` `block_ops` insert (dry run first). Keep the
block id: every item call needs it.

## 3. Upload the images

Per image: `create_upload` with `document_id` = the collection's page, `kind: "image"`,
`dry_run: false`, then straight away `curl -sS -X PUT --data-binary @<file> '<upload_url>'`
(single use, 10 minutes: never create links in bulk and PUT later). Record `key,asset_id`
in an assets CSV as you go, so a failure part-way resumes from where it stopped.

## 4. Load the items

```bash
python build_items.py index.csv assets.csv out/ --fields name,near,state,kind,lot \
  --image crop --location where --status todo
```

Pass each `out/batch-N.json` as `changes` to `update_collection_items` (at most 200 per
call), dry run first. `--status` sets every item's status: use it on the first load
only. On a refresh leave it off so the team's verdicts stay.

## 5. Refresh and change later

- **Upsert by key** updates in place and keeps status, owner, comments and history.
- **Keys are never renamed.** A change that names an item's `id` with a different
  `key` is refused as `key_mismatch`, and so is an unknown `id` with a known key. To
  replace an item (a new pick takes a slot), create a new item with its own key and set
  the old one to the drop status.
- Explain a verdict with `comment_on_item`, not in a field. Mention a teammate as
  `@[Name](ws:<workspace id>)`.
- **Read the team's verdicts back** with `collection_items`: filter by `status`; add
  `comments: N` for each item's latest comments (the reasons); pass one item's `key` (or
  `id`) for its whole history, comments included.
- **On a map:** an `onecell.map` block with the collection as a layer, coloured By
  status, on this page or another page in the same cell (see the onecell-map skill). It
  shows to signed-in readers only: a public page needs an uploaded snapshot instead.

## 6. Check

`collection_items` with `limit` and `status` to spot-check counts per status and a few
items' fields. Open the page: cards show their images, the board groups by status, and
an item opens with its full image. A collection's items show only inside onecell, to
people who can open the page, never on public or share pages. Report the link
`https://onecell.io/cells/{cellSlug}/{documentId}`.
