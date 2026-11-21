"""Server web monitoring sederhana (hanya pustaka standar Python).

Jalankan  : python server.py            -> http://localhost:8000
Kirim data: POST /api/data  {"suhu_c": 28.5, "tegangan_v": 3.12}
Baca data : GET  /api/data?limit=100
"""
import json
import os
import sqlite3
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "data.db")
STATIC = os.path.join(BASE, "static")
PORT = int(os.environ.get("PORT", 8000))


def db():
    c = sqlite3.connect(DB)
    c.execute("CREATE TABLE IF NOT EXISTS baca (ts REAL, suhu_c REAL, tegangan_v REAL)")
    return c


class Handler(BaseHTTPRequestHandler):
    def _json(self, obj, code=200):
        b = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path.startswith("/api/data"):
            limit = 100
            if "limit=" in self.path:
                try:
                    limit = max(1, min(1000, int(self.path.split("limit=")[1].split("&")[0])))
                except ValueError:
                    pass
            conn = db()
            rows = conn.execute(
                "SELECT ts,suhu_c,tegangan_v FROM baca ORDER BY ts DESC LIMIT ?", (limit,)
            ).fetchall()
            conn.close()
            rows.reverse()
            return self._json([{"ts": r[0], "suhu_c": r[1], "tegangan_v": r[2]} for r in rows])
        f = os.path.join(STATIC, "index.html")
        if self.path in ("/", "/index.html") and os.path.exists(f):
            b = open(f, "rb").read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)
            return
        self._json({"error": "tidak ditemukan"}, 404)

    def do_POST(self):
        if self.path != "/api/data":
            return self._json({"error": "tidak ditemukan"}, 404)
        try:
            n = int(self.headers.get("Content-Length", 0))
            d = json.loads(self.rfile.read(n))
            suhu, teg = float(d["suhu_c"]), float(d["tegangan_v"])
        except (ValueError, KeyError, json.JSONDecodeError):
            return self._json({"error": "format salah"}, 400)
        conn = db()
        conn.execute("INSERT INTO baca VALUES (?,?,?)", (time.time(), suhu, teg))
        conn.commit()
        conn.close()
        self._json({"ok": True}, 201)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    db().close()
    print(f"Server jalan di http://localhost:{PORT}")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
