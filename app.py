import base64
import gzip
from pathlib import Path

from flask import Flask, Response, jsonify, request

from crawler import SCrawler

app = Flask(__name__)

_FRONTEND_PARTS = [
    Path("static/frontend.b64.001"),
    Path("static/frontend.b64.002"),
    Path("static/frontend.b64.003"),
    Path("static/frontend.b64.004"),
]


def _frontend_html() -> bytes:
    encoded = "".join(part.read_text(encoding="utf-8").strip() for part in _FRONTEND_PARTS)
    return gzip.decompress(base64.b64decode(encoded))


@app.get("/")
def index():
    return Response(_frontend_html(), mimetype="text/html")


@app.get("/health")
def health():
    return jsonify({"ok": True, "service": "s-crawler"})


@app.post("/crawl")
def crawl():
    body = request.get_json(silent=True) or {}
    url = body.get("url")
    if not url:
        return jsonify({"ok": False, "error": "url is required"}), 400

    max_depth = body.get("max_depth", 5)
    same_domain = body.get("same_domain", True)

    try:
        max_depth = int(max_depth)
        if max_depth < 0 or max_depth > 10:
            raise ValueError("max_depth must be between 0 and 10")
        result = SCrawler(max_depth=max_depth, same_domain=bool(same_domain)).crawl(url)
        return jsonify({"ok": True, "result": result})
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"ok": False, "error": f"{type(exc).__name__}: {exc}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
