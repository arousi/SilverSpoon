"""Headless unit checks for provider/host routing. Run: python test_providers.py

Pins the invariant behind the normalized download logic: FuckingFast and
DataNodes links go through the Turnstile/CAPTCHA solver; every other host is a
plain direct download.
"""
import providers as P


def test_resolver_hosts_need_resolution():
    for link in (
        "https://fuckingfast.co/abc123",
        "https://www.fuckingfast.co/abc123#file.rar",
        "https://datanodes.to/xyz",
        "https://cdn.datanodes.to/d/xyz",   # subdomain of a resolver host
        "http://fuckingfast.co/x",
    ):
        assert P.needs_resolution(link) is True, link


def test_general_hosts_are_direct():
    for link in (
        "https://example.com/file.zip",
        "https://github.com/o/r/releases/download/v1/x.zip",
        "https://objects.githubusercontent.com/…/SilverSpoon.zip",
        "https://notfuckingfast.co.evil.com/x",   # not the real host
        "https://mydatanodes.to.example.com/x",    # not a datanodes.to subdomain
    ):
        assert P.needs_resolution(link) is False, link


def test_malformed_never_crashes():
    for bad in ("", "not a url", "ftp://", "://///", None if False else "javascript:void"):
        assert P.needs_resolution(bad) is False, bad


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} passed")
