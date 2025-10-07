# -----------------------------------------------------------------------------
# Copyright (c) 2025 pxwild. All Rights Reserved.
# pxwild PROPRIETARY AND CONFIDENTIAL — NOT FOR MODIFICATION OR REDISTRIBUTION.
#
# This software and its source code are proprietary to pxwild. Unauthorized
# copying, modification, distribution, decompilation, reverse engineering, or
# creation of derivative works is strictly prohibited without prior written
# permission from pxwild. Any attempt to modify or remove this notice is a
# material breach of the license and will be acted upon to the fullest extent
# permitted by law.
# -----------------------------------------------------------------------------

import argparse
import json
import os
import re
from datetime import datetime

try:
    from PIL import Image, ExifTags
except Exception:
    Image = None
try:
    import exifread
except Exception:
    exifread = None

def read_exif_pillow(path):
    out = {}
    if not Image:
        return out
    try:
        with Image.open(path) as img:
            info = img._getexif() or {}
            tag_map = {ExifTags.TAGS.get(k, k): v for k, v in info.items()}
            out.update(tag_map)
            out["ImageSize"] = img.size
            out["Format"] = img.format
            out["Mode"] = img.mode
    except Exception:
        pass
    return out

def read_exif_exifread(path):
    out = {}
    if not exifread:
        return out
    try:
        with open(path, 'rb') as f:
            tags = exifread.process_file(f, details=False)
            for k, v in tags.items():
                out[str(k)] = str(v)
    except Exception:
        pass
    return out

def extract_gps(exif_dict):
    def _to_deg(values):
        try:
            d = float(values[0][0]) / float(values[0][1])
            m = float(values[1][0]) / float(values[1][1])
            s = float(values[2][0]) / float(values[2][1])
            return d + (m / 60.0) + (s / 3600.0)
        except Exception:
            return None
    lat = lon = None
    try:
        gps = exif_dict.get('GPSInfo') or exif_dict.get('GPS')
        if gps:
            lat = _to_deg(gps.get(2) or gps.get('GPSLatitude'))
            lon = _to_deg(gps.get(4) or gps.get('GPSLongitude'))
            if gps.get(1) in ['S', 'South']:
                lat = -lat if lat else None
            if gps.get(3) in ['W', 'West']:
                lon = -lon if lon else None
    except Exception:
        pass
    return lat, lon

def scan_path(path):
    files = []
    if os.path.isdir(path):
        for root, _, names in os.walk(path):
            for n in names:
                if re.search(r"\.(jpg|jpeg|png|tiff|gif)$", n, re.I):
                    files.append(os.path.join(root, n))
    elif os.path.isfile(path):
        files.append(path)
    return files

def analyze_file(path):
    exif_pillow = read_exif_pillow(path)
    exif_other = read_exif_exifread(path)
    merged = {**exif_other, **exif_pillow}
    lat, lon = extract_gps(merged)
    created = merged.get('DateTimeOriginal') or merged.get('EXIF DateTimeOriginal')
    return {
        "file": path,
        "created": created,
        "gps": {"lat": lat, "lon": lon},
        "meta": merged,
    }

def main():
    parser = argparse.ArgumentParser(description="Automated Image Forensics & Geo-Timeline Builder")
    parser.add_argument("--target", help="Image file or directory", required=False)
    args = parser.parse_args()

    target = args.target if args.target else input("\n[?] Enter image file or directory: ").strip()
    if not target:
        print("[!] No target provided!")
        return

    files = scan_path(target)
    if not files:
        print("[!] No images found")
        return

    print(f"\n[*] Analyzing {len(files)} file(s)")
    results = []
    for p in files:
        results.append(analyze_file(p))

    def _key(r):
        ts = r.get("created") or "9999:99:99 99:99:99"
        return ts
    results.sort(key=_key)

    out = {
        "analyzed_at": datetime.utcnow().isoformat() + "Z",
        "count": len(results),
        "items": results,
    }
    out_file = f"image_timeline_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"[+] Saved timeline JSON to {out_file}")

if __name__ == "__main__":
    main()

