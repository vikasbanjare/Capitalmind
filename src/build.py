"""Build index.html from src/template.html: inlines the logo SVG and the 60-video dataset."""
import json, pathlib, re, sys
root = pathlib.Path(__file__).resolve().parent.parent
tpl = (root / "src/template.html").read_text()
logo = (root / "assets/logo.svg").read_text().strip()
data = json.dumps(json.loads((root / "src/videos.json").read_text()), ensure_ascii=False)
import base64
fonts = "".join(
    '@font-face{font-family:"Poppins";font-style:normal;font-weight:%d;font-display:swap;src:url(data:font/woff2;base64,%s) format("woff2");}\n'
    % (w, base64.b64encode((root / f"assets/fonts/poppins-{w}.woff2").read_bytes()).decode())
    for w in (400, 500, 600, 700))
html = tpl.replace("{{FONTS}}", fonts).replace("{{LOGO}}", logo).replace("{{DATA}}", data)
(root / "index.html").write_text(html)
# Artifact copy: the artifact host supplies its own doctype/html/head/body skeleton.
if len(sys.argv) > 1:
    frag = re.sub(r"<!doctype html>\s*|</?html[^>]*>\s*|</?head>\s*|</?body>\s*", "", html, flags=re.I)
    frag = re.sub(r'<meta charset[^>]*>\s*|<meta name="viewport"[^>]*>\s*', "", frag)
    pathlib.Path(sys.argv[1]).write_text(frag)
print("built", len(html), "bytes")
