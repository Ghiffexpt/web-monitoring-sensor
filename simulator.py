"""Pengganti sensor untuk uji dashboard tanpa hardware. Hentikan dengan Ctrl+C."""
import json
import math
import random
import time
import urllib.request

URL = "http://localhost:8000/api/data"
t = 0
while True:
    suhu = 28 + 3 * math.sin(t / 20) + random.uniform(-0.3, 0.3)
    teg = 3.3 + 0.1 * math.sin(t / 7) + random.uniform(-0.02, 0.02)
    body = json.dumps({"suhu_c": round(suhu, 2), "tegangan_v": round(teg, 3)}).encode()
    req = urllib.request.Request(URL, body, {"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=5).read()
    print("kirim", round(suhu, 2), round(teg, 3))
    t += 1
    time.sleep(2)
