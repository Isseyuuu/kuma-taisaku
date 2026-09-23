"""Read-only structural checks for the bear-site handoff."""

from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://isseyuuu.github.io/kuma-taisaku/"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.alternates = {}
        self.json_scripts = []
        self.in_json = False
        self.json_text = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if key in attrs:
                self.links.append(attrs[key])
        if tag == "link" and attrs.get("rel") == "alternate" and "hreflang" in attrs:
            self.alternates[attrs["hreflang"]] = attrs.get("href")
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.in_json = True
            self.json_text = ""

    def handle_data(self, data):
        if self.in_json:
            self.json_text += data

    def handle_endtag(self, tag):
        if tag == "script" and self.in_json:
            self.json_scripts.append(self.json_text)
            self.in_json = False


def main():
    errors = []
    pages = list(ROOT.rglob("*.html"))
    parsed_pages = {}
    for page in pages:
        raw = page.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            errors.append(f"BOM: {page.relative_to(ROOT)}")
        parser = PageParser()
        parser.feed(raw.decode("utf-8"))
        parsed_pages[page.relative_to(ROOT).as_posix()] = parser
        for block in parser.json_scripts:
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                errors.append(f"JSON-LD: {page.relative_to(ROOT)}: {exc}")
        for link in parser.links:
            parsed = urlsplit(link)
            if parsed.scheme or link.startswith("//"):
                continue
            target = (page.parent / unquote(parsed.path)).resolve() if parsed.path else page
            if not target.exists():
                errors.append(f"Missing local target: {page.relative_to(ROOT)} -> {link}")
            elif parsed.fragment and target == page and parsed.fragment not in parser.ids:
                errors.append(f"Missing anchor: {page.relative_to(ROOT)} -> {link}")
    for left, right in [
        ("index.html", "en/index.html"),
        ("articles/kuma-basics.html", "en/kuma-basics.html"),
        ("articles/where-to-hike.html", "en/where-to-hike.html"),
    ]:
        for language in ("ja", "en", "x-default"):
            if parsed_pages[left].alternates.get(language) != parsed_pages[right].alternates.get(language):
                errors.append(f"Hreflang mismatch: {left} <> {right}, {language}")
    tree = ET.parse(ROOT / "sitemap.xml")
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    for item in tree.findall(f"{ns}url/{ns}loc"):
        url = item.text or ""
        if not url.startswith(BASE):
            errors.append(f"Unexpected sitemap URL: {url}")
            continue
        rel = url[len(BASE):]
        target = ROOT / rel
        if target.is_dir():
            target /= "index.html"
        if not target.exists():
            errors.append(f"Missing sitemap target: {url}")
    print(f"Checked {len(pages)} HTML files and sitemap.xml")
    for error in errors:
        print("ERROR:", error)
    if errors:
        raise SystemExit(1)
    print("Structural checks passed (not a content or safety review).")


if __name__ == "__main__":
    main()
