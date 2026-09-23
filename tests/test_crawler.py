from crawler import normalize_url, same_host


def test_normalize_url():
    assert normalize_url("https://example.com/a", "/b#x") == "https://example.com/b"


def test_reject_non_http():
    assert normalize_url("https://example.com", "mailto:test@example.com") is None


def test_same_host():
    assert same_host("https://example.com/a", "example.com")
    assert not same_host("https://other.com/a", "example.com")
