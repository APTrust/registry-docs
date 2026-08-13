#!/usr/bin/env python3
"""Build the redirect-only site that gets published to the gh-pages branch.

The Registry guide now lives on the unified documentation site at
https://docs.aptrust.org/registry-docs/, which is built by the
APTrust/aptrust-docs repo from the markdown in this repo's docs/ directory.

The old standalone site at https://aptrust.github.io/registry-docs/ no longer
serves the guide. Instead it serves one redirect stub per page, plus a catch-all
404 page, so that existing bookmarks and inbound links land on the real site.

The URL mapping is a pure prefix swap, and it holds for images and other assets
as well as for pages:

    https://aptrust.github.io/registry-docs/<path>
      -> https://docs.aptrust.org/registry-docs/<path>

Note that the '/registry-docs/' segment of NEW_BASE comes from `site_name` in
mkdocs.yml, not from the name of this repo. aptrust-docs pulls this repo's
mkdocs.yml in through mkdocs-monorepo-plugin, which slugifies `site_name` to
build the path. So renaming `site_name: Registry Docs` moves the guide on the
unified site, and NEW_BASE below has to be updated to match.

GitHub Pages cannot issue an HTTP 301, so each stub combines an instant meta
refresh, a rel=canonical link, and a JS location.replace. Search engines treat
that combination as a permanent redirect.

Usage:

    python3 scripts/build_redirects.py [output_dir]

Defaults to writing ./build. Stdlib only, so CI needs no pip install.
"""

import html
import shutil
import sys
from pathlib import Path

# Path GitHub Pages serves this repo under, e.g. aptrust.github.io/registry-docs/.
# Used by 404.html to strip the old base off the incoming path.
OLD_PREFIX = "/registry-docs/"

# Where the guide lives now. Must end with a slash.
NEW_BASE = "https://docs.aptrust.org/registry-docs/"

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "build"

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page moved &mdash; APTrust Registry Docs</title>
<link rel="canonical" href="{target}">
<meta http-equiv="refresh" content="0; url={target}">
<style>{style}</style>
</head>
<body>
<main>
<h1>This page has moved</h1>
<p>The APTrust Registry documentation now lives on the
<a href="{target}">unified documentation site</a>.</p>
<p>If you are not redirected automatically, go to:<br>
<a href="{target}">{target_text}</a></p>
</main>
<script>
// Runs ahead of the meta refresh. Unlike the refresh it carries the query
// string and fragment across, so deep links to a heading still work, and
// location.replace keeps this stub out of the back-button history.
location.replace({target_js} + location.search + location.hash);
</script>
</body>
</html>
"""

NOT_FOUND_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page moved &mdash; APTrust Registry Docs</title>
<link rel="canonical" href="{new_base}">
<meta http-equiv="refresh" content="0; url={new_base}">
<style>{style}</style>
</head>
<body>
<main>
<h1>This documentation has moved</h1>
<p>The APTrust Registry documentation now lives on APTrust's
<a href="{new_base}">unified documentation site</a>. You should be redirected
there automatically.</p>
<p>If you are not redirected, or if the page you were looking for is no longer
at the same address, start from the documentation home page and use the search
or navigation to find what you need:<br>
<a href="{new_base}">{new_base_text}</a></p>
</main>
<script>
// GitHub Pages serves this file for any path without a stub of its own: old
// image URLs, mkdocs asset URLs, and any page removed after the redirect site
// was last built. The path structure is identical on the new site, so swapping
// the base prefix is enough.
(function () {{
  var oldPrefix = {old_prefix_js};
  var newBase = {new_base_js};
  var path = location.pathname;
  var target = newBase;
  if (path.indexOf(oldPrefix) === 0) {{
    target = newBase + path.slice(oldPrefix.length);
  }}
  location.replace(target + location.search + location.hash);
}})();
</script>
</body>
</html>
"""

STYLE = (
    "body{font-family:system-ui,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;"
    "line-height:1.5;margin:0;padding:2rem;color:#1a1a1a;background:#fff}"
    "main{max-width:40rem;margin:0 auto}"
    "h1{font-size:1.5rem}"
    "a{color:#0b4f9c}"
)


def js_string(value):
    """Render a Python string as a JS string literal safe inside <script>."""
    # </ would end the script element early; \x3c keeps it inert.
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("</", "<\\/") + '"'


def url_path_for(md_file):
    """Map a docs/ markdown file to its mkdocs URL path.

    mkdocs runs with use_directory_urls (the default), so pages are served from
    directories. The returned path is relative to the site root and, when
    non-empty, ends with a slash:

        docs/index.md                  -> ""
        docs/structure.md              -> "structure/"
        docs/security/index.md         -> "security/"
        docs/restoration/spot-tests.md -> "restoration/spot-tests/"
    """
    relative = md_file.relative_to(DOCS_DIR)
    parts = list(relative.parts[:-1])
    if relative.stem != "index":
        parts.append(relative.stem)
    return "".join(part + "/" for part in parts)


def write_page(output_dir, url_path):
    target = NEW_BASE + url_path
    destination = output_dir / url_path / "index.html"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        PAGE_TEMPLATE.format(
            target=html.escape(target, quote=True),
            target_text=html.escape(target),
            target_js=js_string(target),
            style=STYLE,
        ),
        encoding="utf-8",
    )
    return target


def write_not_found(output_dir):
    (output_dir / "404.html").write_text(
        NOT_FOUND_TEMPLATE.format(
            new_base=html.escape(NEW_BASE, quote=True),
            new_base_text=html.escape(NEW_BASE),
            new_base_js=js_string(NEW_BASE),
            old_prefix_js=js_string(OLD_PREFIX),
            style=STYLE,
        ),
        encoding="utf-8",
    )


def main():
    output_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_OUTPUT_DIR

    if not DOCS_DIR.is_dir():
        sys.exit("error: {} not found".format(DOCS_DIR))

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    # Walk the filesystem rather than mkdocs.yml's nav, so a page can never be
    # left without a redirect just because the nav drifted out of sync. This
    # also skips the nav's external links, which have no page to redirect.
    md_files = sorted(DOCS_DIR.rglob("*.md"))
    if not md_files:
        sys.exit("error: no markdown files found under {}".format(DOCS_DIR))

    for md_file in md_files:
        target = write_page(output_dir, url_path_for(md_file))
        print("{} -> {}".format(md_file.relative_to(REPO_ROOT), target))

    write_not_found(output_dir)

    # Without this, Pages runs the tree through Jekyll, which skips files and
    # directories whose names start with an underscore.
    (output_dir / ".nojekyll").write_text("", encoding="utf-8")

    print("\n{} redirect pages written to {}".format(len(md_files), output_dir))


if __name__ == "__main__":
    main()
