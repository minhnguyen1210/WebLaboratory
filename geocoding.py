import requests
import time

NOMINATIM = "https://nominatim.openstreetmap.org"
UA = {"User-Agent": "VietnamPlace/1.0 (contact: bsssdd24@gmail.com)"}

def geocode(q):
    time.sleep(0.1)
    r = requests.get(f"{NOMINATIM}/search", params={
        "q": q, "format": "json", "limit": 1, "addressdetails": 1
    }, headers=UA, timeout=60)
    r.raise_for_status()
    data = r.json()
    if not data:
        return None
    item = data[0]
    return float(item["lat"]), float(item["lon"]), item.get("display_name")

