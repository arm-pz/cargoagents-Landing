"""Fill the page template and write index.html. Run from anywhere in the repo."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
out = open(ROOT + "src/page.src.html", encoding="utf-8").read()
out = out.replace("{{LANDMASK}}", open(ROOT + "src/landmask.b64").read().strip())
assert "{{" not in out, re.findall(r"\{\{[^}]+\}\}", out)
open(ROOT + "index.html", "w", encoding="utf-8").write(out)
print("index.html", len(out), "bytes")
