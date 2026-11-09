"""
Build update_collection_items change batches from an index CSV (one row
per item) and an assets CSV (key,asset_id: the image uploaded for that
item), ready to pass as `changes`, at most 200 per call.

    python build_items.py index.csv assets.csv out_dir \
        --fields name,near,state,kind,hh,lot,alike,events \
        --image crop --location where --status todo

Only the columns named in --fields become item fields. --location packs
the lat/lng columns into a location field. Numbers are written as
numbers and blanks are left out, so a re-run never clears a field by
accident. Rows without an uploaded image keep their other fields.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

BATCH = 200


def value(v: str):
    if v is None or v == "":
        return None
    try:
        f = float(v)
    except ValueError:
        return v
    if math.isnan(f):
        return None
    return int(f) if f.is_integer() else round(f, 2)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("index")
    ap.add_argument("assets")
    ap.add_argument("out_dir")
    ap.add_argument("--key", default="key")
    ap.add_argument("--fields", required=True, help="comma-separated index columns to send as fields")
    ap.add_argument("--image", help="the collection's image field key")
    ap.add_argument("--location", help="the collection's location field key (reads --lat/--lng)")
    ap.add_argument("--lat", default="lat")
    ap.add_argument("--lng", default="lng")
    ap.add_argument("--status", help="status for new items, e.g. todo (omit to leave statuses alone)")
    args = ap.parse_args()

    with open(args.assets, newline="") as f:
        assets = {r["key"]: r["asset_id"] for r in csv.DictReader(f)}
    keep = [c for c in args.fields.split(",") if c]
    changes, no_image = [], 0
    with open(args.index, newline="") as f:
        for pos, row in enumerate(csv.DictReader(f), 1):
            fields = {c: v for c in keep if (v := value(row.get(c))) is not None}
            if args.location and value(row.get(args.lat)) is not None:
                fields[args.location] = {"lat": float(row[args.lat]), "lng": float(row[args.lng])}
            if args.image:
                if row[args.key] in assets:
                    fields[args.image] = assets[row[args.key]]
                else:
                    no_image += 1
            change = {"op": "upsert", "key": row[args.key], "position": pos, "fields": fields}
            if args.status:
                change["status"] = args.status
            changes.append(change)

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for i in range(0, len(changes), BATCH):
        (out / f"batch-{i // BATCH + 1}.json").write_text(json.dumps(changes[i:i + BATCH], separators=(",", ":")))
    print(f"{len(changes)} items in {math.ceil(len(changes) / BATCH)} batch(es) -> {out}"
          + (f" ({no_image} without an image)" if no_image else ""))


if __name__ == "__main__":
    main()
