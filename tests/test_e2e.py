import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

import pytest

from app import app
from crawler import SCrawler


PAGES = {
    "/": """<!doctype html><html><head><title>Root</title></head><body>
        <a href="/a">A</a>
        <a href="/a#duplicate">A duplicate fragment</a>
        <script>document.body.insertAdjacentHTML('beforeend','<a href="/js">JS Link</a>')</script>
    </body></html>""",
    "/a": """<!doctype html><html><head><title>A</title></head><body><a href="/b">B</a></body></html>""",
    "/js": """<!doctype html><html><head><title>JS</title></head><body>Rendered link target</body></html>""",
    "/b": """<!doctype html><html><head><title>B</title></head><body>Level two</body></html>""",
}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        body = PAGES.get(path)
        if body is None:
            self.send_response(404)
            self.end_headers()
            return
        encoded = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format, *args):
        return


@pytest.fixture()
def site():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        yield base
    finally:
        server.shutdown()
        thread.join(timeout=2)


def test_real_browser_level_model_js_and_dedup(site):
    result = SCrawler(max_depth=2, same_domain=True).crawl(site + "/")
    by_path = {urlparse(page["url"]).path: page for page in result["pages"]}

    assert by_path["/"]["level"] == 0
    assert by_path["/a"]["level"] == 1
    assert by_path["/js"]["level"] == 1
    assert by_path["/b"]["level"] == 2
    assert sum(1 for page in result["pages"] if urlparse(page["url"]).path == "/a") == 1
    assert result["stats"]["errors"] == 0
    assert result["stats"]["levels_reached"] == 2


def test_frontend_serves_and_api_executes_real_crawl(site):
    client = app.test_client()

    frontend = client.get("/")
    assert frontend.status_code == 200
    assert b"<html" in frontend.data.lower()

    response = client.post("/crawl", json={"url": site + "/", "max_depth": 1, "same_domain": True})
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["ok"] is True
    assert payload["result"]["stats"]["errors"] == 0
    assert payload["result"]["stats"]["levels_reached"] == 1
    assert any(urlparse(page["url"]).path == "/js" for page in payload["result"]["pages"])
