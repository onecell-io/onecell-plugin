"""
Turn a CSV with latitude/longitude columns into a GeoJSON layer file for a
onecell map (an onecell.map layer, or a sandbox map).

    python to_geojson.py sites.csv sites.geojson --props name,status,households
    python to_geojson.py sites.csv sites.geojson --lat latitude --lng longitude --round 4

Only the columns named in --props become feature properties, so nothing else in
the CSV leaves the machine. Rows without coordinates are skipped and counted.
"""
from __future__ import annotations

import argparse
import csv
import json
import math


def number(v: str):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return v
    if math.isnan(f):
        return None
    return int(f) if f.is_integer() else f


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--lat", default="lat")
    ap.add_argument("--lng", default="lng")
    ap.add_argument("--props", default="", help="comma-separated columns to keep as properties")
    ap.add_argument("--round", type=int, default=5, help="coordinate decimals (5 is about 1 m)")
    args = ap.parse_args()

    keep = [c for c in args.props.split(",") if c]
    features, skipped = [], 0
    with open(args.src, newline="") as f:
        for row in csv.DictReader(f):
            try:
                lat, lng = float(row[args.lat]), float(row[args.lng])
            except (KeyError, TypeError, ValueError):
                skipped += 1
                continue
            features.append({
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [round(lng, args.round), round(lat, args.round)]},
                "properties": {c: number(row.get(c)) for c in keep},
            })
    with open(args.dst, "w") as f:
        json.dump({"type": "FeatureCollection", "features": features}, f, separators=(",", ":"))
    print(f"{len(features)} features -> {args.dst}" + (f" ({skipped} rows without coordinates skipped)" if skipped else ""))


if __name__ == "__main__":
    main()
