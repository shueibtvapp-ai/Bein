import time
import os
from flask import Flask, Response, request
import requests

app = Flask(__name__)
session = requests.Session()
CACHE_TTL = 30
manifest_cache = {"content": None, "ts": 0}

def read_stream_file():
    try:
        return open("stream.txt").read().strip()
    except Exception:
        return ""

def get_manifest(url):
    now = time.time()
    if now - manifest_cache["ts"] < CACHE_TTL and manifest_cache["content"]:
        return manifest_cache["content"]
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.youtube.com/", "Origin": "https://www.youtube.com"}
    try:
        r = session.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            manifest_cache["content"] = r.content
            manifest_cache["ts"] = now
            return manifest_cache["content"]
    except Exception:
        return None
    return None

@app.route("/")
def home():
    return "BEIN SERVER IS RUNNING (Use /bein)"

@app.route("/bein")
def proxy():
    url = read_stream_file()
    if not url:
        return "جاري تهيئة البث حاول مرة أخرى...", 503
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.youtube.com/", "Origin": "https://www.youtube.com"}
    if "Range" in request.headers:
        headers["Range"] = request.headers["Range"]
    try:
        r = session.get(url, headers=headers, stream=True, allow_redirects=True, timeout=15)
    except Exception:
        return "جاري تهيئة البث حاول مرة أخرى...", 503

    def generate():
        try:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    yield chunk
        finally:
            try:
                r.close()
            except Exception:
                pass

    return Response(generate(), status=r.status_code, headers={"Content-Type": r.headers.get("Content-Type", "application/vnd.apple.mpegurl"), "Access-Control-Allow-Origin": "*", "Accept-Ranges": "bytes"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
