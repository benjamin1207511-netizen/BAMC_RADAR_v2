import json, re, sys, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

BASE = Path(__file__).resolve().parents[1] / "site" / "data"
BASE.mkdir(parents=True, exist_ok=True)
KML_URL = "https://www.hko.gov.hk/wxinfo/radars/R4_GIS_rad_256/R4_GIS_server_Radar_256.kml"
HEADERS = {"User-Agent": "BAMC-RADAR/2.0 (public weather imagery viewer)"}

def get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.status, r.headers.get("Content-Type", ""), r.read()

status, ctype, body = get(KML_URL)
if status != 200 or not body.strip():
    raise RuntimeError(f"KML request failed: HTTP {status}, content-type={ctype}")
try:
    root = ET.fromstring(body)
except ET.ParseError as e:
    raise RuntimeError(f"Radar index is not valid XML/KML: {e}")

items = []
for overlay in root.iter():
    if overlay.tag.split("}")[-1] != "GroundOverlay":
        continue
    name = ""
    href = ""
    for child in overlay.iter():
        tag = child.tag.split("}")[-1]
        if tag == "name" and child.text:
            name = child.text.strip()
        elif tag == "href" and child.text:
            href = child.text.strip()
    if href:
        # Prefer timestamp from image filename (YYYYMMDDHHMMSS); then overlay name.
        m = re.search(r"(\d{12,14})", href)
        if not m:
            m = re.search(r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})", name)
        key = m.group(1) if m else ""
        items.append((key, name, urljoin(KML_URL, href)))

if not items:
    raise RuntimeError("KML loaded but contained no GroundOverlay image references.")
items.sort(key=lambda x: x[0])
key, name, image_url = items[-1]
status, image_type, image_bytes = get(image_url)
if status != 200 or not image_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
    raise RuntimeError(f"Latest image did not validate as PNG: HTTP {status}, type={image_type}, bytes={len(image_bytes)}")

(BASE / "hko-radar.png").write_bytes(image_bytes)
meta = {
    "source": "Hong Kong Observatory",
    "index_url": KML_URL,
    "image_url": image_url,
    "filename": image_url.rsplit("/", 1)[-1],
    "time": name or key or datetime.now(timezone.utc).isoformat(),
    "fetched_utc": datetime.now(timezone.utc).isoformat(),
    "content_type": image_type,
    "bytes": len(image_bytes),
}
(BASE / "hko-radar.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(meta, ensure_ascii=False, indent=2))
