#!/usr/bin/env python3
"""
localize-images.py — Download all remote Figma images referenced in index.html
to a local ./images folder and rewrite URLs to relative paths.

Usage:
    python localize-images.py

Run this ONCE after copying the project folder to your computer.
After running, the HTML works fully offline and won't break when Figma's
asset URLs expire (which they do, 7 days after generation).
"""

import os
import re
import sys
import urllib.request

HTML_FILE = "index.html"
IMAGES_DIR = "images"
URL_PATTERN = re.compile(r'https://www\.figma\.com/api/mcp/asset/([0-9a-f-]+)')

# friendly names so the downloaded files are recognizable rather than UUIDs
FRIENDLY_NAMES = {
    "d7bae546-52e4-4686-bc8c-dfb378604232": "hero-quant-trader",
    "9d7e69b3-2411-4bd2-84d1-364f30b532b5": "yuki",
    "85189ef0-a8df-43b4-a5fc-6744e124a055": "clawpay-s1",
    "088584ea-0dd8-45b5-8179-4febbecc2233": "cr-ca-agent",
    "782c81e7-4204-4edc-992d-cca12c2ed739": "clawpay-s2",
    "1f2c1dac-5341-49a3-9142-b60400c7c030": "self-aware-meme",
    "f96a22ef-3554-4182-a9b2-32667a00dd2e": "sam-the-scam",
    "5467522c-8bad-4dad-986b-733476cabba3": "nexus-ai",
    "b06269cb-2a80-4f19-b908-2ccb3db2ffdf": "quant-trader-agent",
    "480956a9-6e51-4224-94c6-56c859c5a375": "apple-agent",
    "02fd47c3-061b-4615-9819-abc29c24483b": "rok",
    "eeefaeb3-9f3c-423d-83ad-ac95021e8d25": "muffins",
    "09798067-3cdc-4b9f-a0a3-0e642f008062": "frenzy",
}


def main():
    if not os.path.exists(HTML_FILE):
        print(f"ERROR: {HTML_FILE} not found in current directory.")
        print(f"Run this script from the folder containing {HTML_FILE}.")
        sys.exit(1)

    os.makedirs(IMAGES_DIR, exist_ok=True)

    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    uuids = set(URL_PATTERN.findall(html))
    print(f"Found {len(uuids)} unique image references.\n")

    replacements = {}
    for i, uuid in enumerate(sorted(uuids), 1):
        friendly = FRIENDLY_NAMES.get(uuid, uuid)
        local_path = f"{IMAGES_DIR}/{friendly}.png"
        full_local = os.path.join(IMAGES_DIR, f"{friendly}.png")

        if os.path.exists(full_local):
            print(f"[{i}/{len(uuids)}] {friendly}.png — already downloaded, skipping")
            replacements[uuid] = local_path
            continue

        url = f"https://www.figma.com/api/mcp/asset/{uuid}"
        print(f"[{i}/{len(uuids)}] downloading {friendly}.png ...")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            with open(full_local, "wb") as out:
                out.write(data)
            replacements[uuid] = local_path
            print(f"           saved ({len(data) // 1024} KB)")
        except Exception as e:
            print(f"           FAILED: {e}")
            print(f"           Note: Figma asset URLs expire 7 days after generation.")
            print(f"           If this fails, ask the developer to regenerate URLs.")

    if not replacements:
        print("\nNothing was downloaded. Aborting.")
        sys.exit(1)

    new_html = html
    for uuid, local_path in replacements.items():
        new_html = new_html.replace(
            f"https://www.figma.com/api/mcp/asset/{uuid}",
            local_path,
        )

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(new_html)

    print(f"\n✓ Done. {len(replacements)} URLs rewritten in {HTML_FILE}.")
    print(f"✓ Images saved to ./{IMAGES_DIR}/")
    print("\nThe HTML is now fully self-contained and will work offline.")


if __name__ == "__main__":
    main()
