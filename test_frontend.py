"""
Automated Comprehensive Frontend Test Suite for Smart Waste Classification
Validates:
1. Architecture & Vercel deployment configuration (vercel.json)
2. HTML5 syntax, meta viewport, titles, and DOM structure
3. Asset path integrity (CSS, JS, images, CDNs) and absence of unrendered Jinja tags
4. Navigation bar consistency and cross-page links
5. Accessibility (a11y) basics: alt attributes, aria-labels, button names, focus styles
6. Responsive CSS media queries (mobile <520px/<768px, tablet <900px, desktop)
7. Classifier UI elements: upload dropzone, camera, preview, loading state, error alert,
   results panel, confidence meter, disposal advice card, 5-class breakdown, low-confidence warning
8. Dashboard & History DOM hydration elements and Chart.js canvases
9. Quick 1-click test sample assets and metadata integrity
"""

import os
import re
import json
import unittest
from bs4 import BeautifulSoup

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

PAGES = [
    ("index.html", "/"),
    ("classify.html", "/classify"),
    ("dashboard.html", "/dashboard"),
    ("history.html", "/history"),
    ("awareness.html", "/awareness")
]

class FrontendTestSuite(unittest.TestCase):

    def setUp(self):
        self.pages_html = {}
        self.soups = {}
        for filename, route in PAGES:
            filepath = os.path.join(BASE_DIR, filename)
            self.assertTrue(os.path.exists(filepath), f"Missing page: {filename}")
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            self.pages_html[filename] = content
            self.soups[filename] = BeautifulSoup(content, "html.parser")

    def test_vercel_configuration(self):
        """Verify vercel.json exists, is valid JSON, and defines clean routing."""
        vercel_path = os.path.join(BASE_DIR, "vercel.json")
        self.assertTrue(os.path.exists(vercel_path), "vercel.json does not exist!")
        with open(vercel_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        self.assertTrue(config.get("cleanUrls"), "cleanUrls should be enabled")
        self.assertIn("rewrites", config)
        rewrites = {r["source"]: r["destination"] for r in config["rewrites"]}

        expected_rewrites = {
            "/classify": "/classify.html",
            "/dashboard": "/dashboard.html",
            "/history": "/history.html",
            "/awareness": "/awareness.html"
        }
        for src, dest in expected_rewrites.items():
            self.assertIn(src, rewrites, f"Missing rewrite for {src}")
            self.assertEqual(rewrites[src], dest)

        print("PASS: vercel.json verified with clean URLs and page rewrites.")

    def test_html5_structure_and_meta(self):
        """Verify valid HTML5 structure, viewport, and titles on all 5 pages."""
        for filename, soup in self.soups.items():
            html_text = self.pages_html[filename]
            self.assertTrue(html_text.strip().startswith("<!DOCTYPE html>"), f"{filename} missing <!DOCTYPE html>")
            
            # Viewport meta for mobile responsiveness
            viewport = soup.find("meta", attrs={"name": "viewport"})
            self.assertIsNotNone(viewport, f"{filename} missing meta viewport tag")
            self.assertIn("width=device-width", viewport.get("content", ""))

            # Charset
            charset = soup.find("meta", attrs={"charset": True})
            self.assertIsNotNone(charset, f"{filename} missing meta charset tag")

            # Title
            title = soup.find("title")
            self.assertIsNotNone(title, f"{filename} missing <title>")
            self.assertIn("Smart Waste", title.text)

        print(f"PASS: HTML5 doctype, viewport, and meta verified across all {len(PAGES)} pages.")

    def test_no_unrendered_jinja_tags(self):
        """Ensure static HTML files contain zero raw Jinja2 server template tags."""
        jinja_pattern = re.compile(r"\{\{.*?\}\}|\{%.*?%\}")
        for filename, html_text in self.pages_html.items():
            matches = jinja_pattern.findall(html_text)
            self.assertEqual(
                len(matches), 0,
                f"{filename} contains raw Jinja tags: {matches}"
            )
        print("PASS: Verified zero unrendered Jinja tags in static HTML pages.")

    def test_navigation_consistency(self):
        """Verify navigation bar and links consistency across all pages."""
        expected_routes = ["/", "/classify", "/dashboard", "/history", "/awareness"]

        for filename, soup in self.soups.items():
            nav = soup.find("header", class_="navbar")
            self.assertIsNotNone(nav, f"{filename} missing navbar")

            brand = nav.find("a", class_="brand-logo")
            self.assertIsNotNone(brand, f"{filename} missing brand-logo")

            nav_links = nav.find("ul", class_="nav-links")
            self.assertIsNotNone(nav_links, f"{filename} missing .nav-links")

            hrefs = [a.get("href") for a in nav_links.find_all("a")]
            for r in expected_routes:
                self.assertIn(r, hrefs, f"{filename} nav missing link to {r}")

        print("PASS: Navigation header and route links verified across all pages.")

    def test_asset_paths_and_local_integrity(self):
        """Verify CSS, JS, and image paths exist locally or use trusted CDNs."""
        for filename, soup in self.soups.items():
            # Stylesheets
            for link in soup.find_all("link", rel="stylesheet"):
                href = link.get("href", "")
                clean_href = href.split("?")[0]
                if clean_href.startswith("/static/"):
                    local_path = os.path.join(BASE_DIR, clean_href.lstrip("/"))
                    self.assertTrue(os.path.exists(local_path), f"{filename} links missing CSS: {local_path}")
                elif clean_href.startswith("http"):
                    self.assertTrue("cdnjs.cloudflare.com" in href or "cdn.jsdelivr.net" in href)

            # Scripts
            for script in soup.find_all("script", src=True):
                src = script.get("src", "")
                clean_src = src.split("?")[0]
                if clean_src.startswith("/static/"):
                    local_path = os.path.join(BASE_DIR, clean_src.lstrip("/"))
                    self.assertTrue(os.path.exists(local_path), f"{filename} links missing JS: {local_path}")
                elif clean_src.startswith("http"):
                    self.assertTrue("cdn.jsdelivr.net" in src or "cdnjs.cloudflare.com" in src)

        print("PASS: All stylesheet and script asset paths exist locally or on CDNs.")

    def test_accessibility_basics(self):
        """Verify a11y basics: image alt attributes, input accessibility, button text."""
        for filename, soup in self.soups.items():
            # Images
            for img in soup.find_all("img"):
                alt = img.get("alt")
                self.assertIsNotNone(alt, f"{filename} has <img> without alt attribute")
                self.assertGreater(len(alt.strip()), 0, f"{filename} has empty alt text")

            # Inputs
            for inp in soup.find_all("input"):
                has_label = bool(inp.get("aria-label") or inp.get("id"))
                self.assertTrue(has_label, f"{filename} has input without label or aria-label")

            # Buttons
            for btn in soup.find_all("button"):
                text_content = btn.text.strip()
                aria_label = btn.get("aria-label")
                self.assertTrue(bool(text_content or aria_label), f"{filename} has empty button")

        print("PASS: Accessibility basics verified (image alt text, aria-labels, buttons).")

    def test_responsive_css_media_queries(self):
        """Verify style.css contains responsive media queries for mobile, tablet, and desktop."""
        css_path = os.path.join(BASE_DIR, "static", "css", "style.css")
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

        # Check breakpoints
        breakpoints = ["max-width: 520px", "max-width: 860px", "max-width: 900px"]
        for bp in breakpoints:
            self.assertIn(bp, css_content, f"style.css missing responsive breakpoint: {bp}")

        # Check focus ring for keyboard navigation
        self.assertIn(":focus-visible", css_content, "style.css missing :focus-visible rules")

        print("PASS: Responsive CSS media queries (mobile, tablet, desktop) and focus states verified.")

    def test_classifier_page_elements(self):
        """Verify all essential interactive elements on classify.html."""
        soup = self.soups["classify.html"]

        # Input elements
        self.assertIsNotNone(soup.find(id="tabUpload"))
        self.assertIsNotNone(soup.find(id="tabCamera"))
        self.assertIsNotNone(soup.find(id="dropzone"))
        self.assertIsNotNone(soup.find(id="fileInput"))
        self.assertIsNotNone(soup.find(id="cameraStream"))
        self.assertIsNotNone(soup.find(id="btnCapture"))
        self.assertIsNotNone(soup.find(id="btnPredict"))

        # Feedback & Results elements
        self.assertIsNotNone(soup.find(id="emptyState"))
        self.assertIsNotNone(soup.find(id="loadingBox"))
        self.assertIsNotNone(soup.find(id="errorAlert"))
        self.assertIsNotNone(soup.find(id="resultContent"))

        # Feature 3 & 6 elements
        self.assertIsNotNone(soup.find(id="resCategory"))
        self.assertIsNotNone(soup.find(id="resConfidence"))
        self.assertIsNotNone(soup.find(id="confidenceBar"))
        self.assertIsNotNone(soup.find(id="resBinName"))
        self.assertIsNotNone(soup.find(id="resRecyclableTag"))
        self.assertIsNotNone(soup.find(id="resDisposalInstructions"))
        self.assertIsNotNone(soup.find(id="resSegregationSteps"))
        self.assertIsNotNone(soup.find(id="resEcoFact"))
        self.assertIsNotNone(soup.find(id="breakdownList"))
        self.assertIsNotNone(soup.find(id="lowConfidenceWarning"))

        # Demo sample chips
        sample_chips = soup.find_all(class_="chip-btn")
        self.assertEqual(len(sample_chips), 5)
        samples = [chip.get("data-sample") for chip in sample_chips]
        for cat in ["plastic", "paper", "metal", "glass", "organic"]:
            self.assertIn(f"{cat}_sample_1.jpg", samples)

        print("PASS: Waste classifier UI elements, states, recommendation cards, and sample chips verified.")

    def test_dashboard_and_history_hydration_elements(self):
        """Verify DOM hydration IDs in dashboard.html and history.html."""
        dash_soup = self.soups["dashboard.html"]
        self.assertIsNotNone(dash_soup.find(id="statTotalNumber"))
        for cat in ["Plastic", "Paper", "Metal", "Glass", "Organic"]:
            self.assertIsNotNone(dash_soup.find(id=f"statCount{cat}"))
            self.assertIsNotNone(dash_soup.find(id=f"statPct{cat}"))
            self.assertIsNotNone(dash_soup.find(id=f"statBar{cat}"))
        self.assertIsNotNone(dash_soup.find(id="barChartCanvas"))
        self.assertIsNotNone(dash_soup.find(id="donutChartCanvas"))

        hist_soup = self.soups["history.html"]
        self.assertIsNotNone(hist_soup.find(id="historyTableContainer"))
        self.assertIsNotNone(hist_soup.find(id="historyTableBody"))
        self.assertIsNotNone(hist_soup.find(id="historyEmptyState"))
        self.assertIsNotNone(hist_soup.find(id="btnClearHistoryBtn"))

        print("PASS: Dashboard telemetry metrics, Chart.js canvases, and History table elements verified.")

    def test_sample_images_exist(self):
        """Verify sample images exist in sample_test_images directory."""
        sample_dir = os.path.join(BASE_DIR, "sample_test_images")
        for cat in ["plastic", "paper", "metal", "glass", "organic"]:
            path = os.path.join(sample_dir, f"{cat}_sample_1.jpg")
            self.assertTrue(os.path.exists(path), f"Missing sample file: {path}")

        print("PASS: All 5 1-click sample images exist on disk.")


if __name__ == "__main__":
    unittest.main()
