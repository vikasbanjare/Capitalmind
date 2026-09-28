"""Build index.html from src/template.html.

Inlines fonts, the logo, every image (as data URIs, so the page works as a
single file anywhere) and the 60-video dataset.
Usage: python3 src/build.py [extra-output-without-html-skeleton.html]
"""
import base64, json, pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
tpl = (root / "src/template.html").read_text()

def b64(p): return base64.b64encode(p.read_bytes()).decode()

fonts = "".join(
    '@font-face{font-family:"Poppins";font-style:normal;font-weight:%d;font-display:swap;'
    'src:url(data:font/woff2;base64,%s) format("woff2");}\n' % (w, b64(root / f"assets/fonts/poppins-{w}.woff2"))
    for w in (400, 500, 600, 700))
imgs = {p.stem: "data:image/webp;base64," + b64(p) for p in sorted((root / "assets/img").glob("*.webp"))}

used_js = set(re.findall(r"'([a-z0-9-]+)'", tpl)) & set(imgs)
html = tpl.replace("{{FONTS}}", fonts)
html = html.replace("{{LOGO}}", (root / "assets/logo.svg").read_text().strip())
html = re.sub(r"\{\{IMG:([a-z0-9-]+)\}\}", lambda m: imgs[m.group(1)], html)
html = html.replace("{{IMGMAP}}", json.dumps({k: imgs[k] for k in sorted(used_js)}))
html = html.replace("{{DATA}}", json.dumps(json.loads((root / "src/videos.json").read_text()), ensure_ascii=False))
assert "{{" not in html, re.findall(r"\{\{[^}]*\}\}", html)[:5]
(root / "index.html").write_text(html)

if len(sys.argv) > 1:  # artifact copy: host supplies doctype/html/head/body
    frag = re.sub(r"<!doctype html>\s*|</?html[^>]*>\s*|</?head>\s*|</?body>\s*", "", html, flags=re.I)
    frag = re.sub(r'<meta charset[^>]*>\s*|<meta name="viewport"[^>]*>\s*', "", frag)
    pathlib.Path(sys.argv[1]).write_text(frag)
print(f"built {len(html)//1024} KB, {len(imgs)} images, {len(used_js)} in JS map")
