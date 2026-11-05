"""Build ARG (Agriseco) design tokens from the legacy TradeX/Paave export.

Usage: python3 build_arg.py <src_dir> <out_dir>
"""
import colorsys, copy, json, re, sys
from pathlib import Path

SRC, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
load = lambda n: json.load(open(SRC / n, encoding="utf-8"))

BRAND_RED = "#a5000a"

# ---------- helpers ----------
def hsl_hex(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return "#%02x%02x%02x" % tuple(round(x * 255) for x in (r, g, b))

def rename_keys(node, mapping):
    """Recursively rename dict keys using mapping (exact match)."""
    if not isinstance(node, dict):
        return node
    return {mapping.get(k, k): rename_keys(v, mapping) for k, v in node.items()}

def replace_refs(obj, subs):
    s = json.dumps(obj, ensure_ascii=False)
    for a, b in subs:
        s = s.replace(a, b)
    return json.loads(s)

def walk(d, p=()):
    if isinstance(d, dict) and "$value" in d:
        yield p, d
        return
    if isinstance(d, dict):
        for k, v in d.items():
            if not k.startswith("$"):
                yield from walk(v, p + (k,))

def dump(name, data):
    with open(OUT / name, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

# Typos fixed across every file (token names + references)
KEY_FIXES = {
    "Sureface": "Surface",
    "Saperator": "Separator",
    "eff_Saperator": "eff_Separator",
    "Rugular": "Regular",
    "height-largre": "height-large",
    "Text_Button-Main-Green": "Text_Button-Outline",
    "\bRevenue": "Revenue",
}
REF_FIXES = [
    ("{p--Gray.Raven.", "{p--Neutral."),
    (".Sureface}", ".Surface}"),
    (".Saperator}", ".Separator}"),
    (".eff_Saperator}", ".eff_Separator}"),
    ("{P3_Trading Color.", "{P3_Trading_Color."),
    ("{P7_Gradient.Empty Color}", "{P7_Gradient.Empty_Color}"),
    ("{Font.Line_Height.Body}", "{Font.Line_Height.Body_1}"),
]
for grp in ["Display", "Header", "Title", "Body", "Label"]:
    for i in range(1, 5):
        for kind in ["Font_Size", "Line_Height"]:
            REF_FIXES.append((f"{{Font.{kind}.{grp} {i}}}", f"{{Font.{kind}.{grp}_{i}}}"))

# ---------- 1. Primitive: ARG-Color ----------
prim = rename_keys(load("Paave-Color.Mode 1.tokens.json"), KEY_FIXES)

# Agriseco red ramp, 600-M = logo red #A5000A (h 356.4°, l 32.4%)
L = {"50": 97, "100": 93, "200": 86, "300": 76, "400": 64, "500": 48,
     "700": 27, "800": 22, "900": 17, "950": 11}
red = {k: {"$type": "color", "$value": hsl_hex(356.4, 100 if l < 90 else 100, l)} for k, l in L.items()}
red["600-M"] = {"$type": "color", "$value": BRAND_RED}
order = ["50", "100", "200", "300", "400", "500", "600-M", "700", "800", "900", "950"]
prim["p--Primary"] = {"Agri_Red": {k: red[k] for k in order}, **prim["p--Primary"]}

# Agriseco neutral ramp, 11 steps like Tailwind CSS (50 to 950), pure grey (R = G = B).
# Replaces the blue-tinted Gray.Raven of TradeX; lightness of each step stays close to the old ramp so contrast does not change.
NEUTRAL = {"50": "#f7f7f7", "100": "#efefef", "200": "#e2e2e2", "300": "#d0d0d0", "400": "#a8a8a8", "500": "#7d7d7d",
           "600": "#5c5c5c", "700": "#444444", "800": "#2c2c2c", "900": "#1a1a1a", "950": "#0d0d0d"}
prim["p--Neutral"] = {k: {"$type": "color", "$value": v} for k, v in NEUTRAL.items()}
del prim["p--Gray"]

# Agriseco orange ramp (brand header #ea5b2f is step 600-M, same convention as Agri_Red)
OL = {"50": (96, 90), "100": (92, 90), "200": (85, 88), "300": (75, 86), "400": (65, 84), "500": (59, 83),
      "700": (45, 82), "800": (36, 80), "900": (28, 76), "950": (17, 70)}
orange = {k: {"$type": "color", "$value": hsl_hex(14, sat, l)} for k, (l, sat) in OL.items()}
orange["600-M"] = {"$type": "color", "$value": "#ea5b2f"}
prim["p--Primary"] = {"Agri_Orange": {k: orange[k] for k in order}, **prim["p--Primary"]}

# Grayscale (17 steps used by text and dark surfaces): same lightness, no colour cast
for tok in prim["p--Grayscale"].values():
    h = tok["$value"]
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    v = round(colorsys.rgb_to_hls(r, g, b)[1] * 255)
    tok["$value"] = "#%02x%02x%02x" % (v, v, v)

# Alpha.Black re-based on pure black (the old steps leaned teal and blue), same alpha steps
for tok in prim["p--Alpha"]["Black"].values():
    tok["$value"] = "#000000" + tok["$value"][7:]

# Alpha.Primary re-based on brand red, same alpha steps
for k, tok in prim["p--Alpha"]["Primary"].items():
    tok["$value"] = BRAND_RED + tok["$value"][7:]

# Brand colours sampled from the new Agriseco logo and agriseco.com.vn (.btn-orange)
prim = {
    "p--Brand": {
        "Header_Start": {"$type": "color", "$value": "#ea5b2f"},
        "Header_End": {"$type": "color", "$value": "#f33a44"},
        "Gradient_Start": {"$type": "color", "$value": "#ff6a00"},  # điểm đầu gradient ô icon dịch vụ (--arg-gradient-service, chủ dự án chốt)
        "Orange": {"$type": "color", "$value": "#f28021"},
        "Yellow": {"$type": "color", "$value": "#fec015"},
        "Amber": {"$type": "color", "$value": "#faae42"},
        "Gold": {"$type": "color", "$value": "#f6e92d"},
        "Orange_Red": {"$type": "color", "$value": "#f15b2c"},
        "Agri_Red": {"$type": "color", "$value": BRAND_RED},
    },
    **prim,
}
dump("ARG-Color.Mode 1.tokens.json", prim)

# ---------- 2. Theme: ARG light / dark ----------
PRIMARY_OLD = "{p--Primary.Royal_Blue.600-M}"
PRIMARY_NEW = "{p--Primary.Agri_Red.600-M}"

def theme(fname, dark):
    t = rename_keys(load(fname), KEY_FIXES)
    t = replace_refs(t, REF_FIXES + [(PRIMARY_OLD, PRIMARY_NEW)])
    # Literal greys in the theme (dark surfaces) leaned blue: keep the lightness, drop the colour cast
    for _, tok in walk(t):
        v = tok["$value"]
        if isinstance(v, str) and re.fullmatch(r"#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?", v):
            r, g, b = (int(v[i:i + 2], 16) / 255 for i in (1, 3, 5))
            hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
            if 0 < ss < 0.3:
                n = round(ll * 255)
                tok["$value"] = "#%02x%02x%02x" % (n, n, n) + v[7:]
    # Buy / Sell buttons own their colours (market up / down), never Primary
    for side, trade in (("Buy", "Up-Light"), ("Sell", "Down-Light")):
        t["P4_Action"][f"{side}_Button"] = {
            f"Button-{side}": {"$type": "color", "$value": f"{{P3_Trading_Color.{trade}.Increase}}"},
            f"Button-{side}-Disable": {"$type": "color", "$value": f"{{P3_Trading_Color.{trade}.Soft-Increase}}"},
            f"Text_Button-{side}": {"$type": "color", "$value": "{p--Grayscale.100}"},
            f"Text_Button-{side}-Disable": {"$type": "color", "$value": "{P2_UI_Color.Text.On_Bright.Text-Disable}"},
        }
    if dark:
        # #A5000A on #17181C is ~2.3:1 — lift primary text to a readable step
        a = t["P4_Action"]
        light_red = "{p--Primary.Agri_Red.400}"
        a["Secondary_Button"]["Text_Button-Secondary"]["$value"] = light_red
        a["Outline_Button"]["Text_Button-Outline"]["$value"] = light_red
        a["Text_Button_Link"]["Text_Button"]["$value"] = light_red
    return t

light = theme("Theme.TradeX_Lightmode.tokens.json", False)
dark = theme("Theme.TradeX_Darkmode.tokens.json", True)
dump("Theme.ARG_Lightmode.tokens.json", light)
dump("Theme.ARG_Darkmode.tokens.json", dark)

# ---------- 3. Spacing / Typography / Styles ----------
spacing = rename_keys(load("Spacing.Mode 1.tokens.json"), KEY_FIXES)
hs = spacing["d--borders"]["height-size"]
hs["height-xl"] = {"$type": "dimension", "$value": "{d--spacing.11x}"}
hs["height-xxl"] = {"$type": "dimension", "$value": "{d--spacing.12x}"}
dump("Spacing.Mode 1.tokens.json", spacing)

typo = rename_keys(load("Typography.Pretendard.tokens.json"), KEY_FIXES)
lh = typo["Font"]["Line_Height"]
typo["Font"]["Line_Height"] = {("Body_1" if k == "Body" else k): v for k, v in lh.items()}
dump("Typography.Pretendard.tokens.json", typo)

text_styles = replace_refs(load("text.styles.tokens.json"), REF_FIXES)
color_styles = replace_refs(load("color.styles.tokens.json"), REF_FIXES)
effect_styles = rename_keys(replace_refs(load("effect.styles.tokens.json"), REF_FIXES), {"eff-Saperator": "eff-Separator"})
# Primary button gradient, same as the header (--top-nav-background-4) on agriseco.com.vn
color_styles["Gradient"]["Primary Button - Header gradient"] = {
    "$type": "gradient",
    "$value": {"type": "linear", "angle": 90, "stops": [
        {"color": "{p--Brand.Header_Start}", "position": 0},
        {"color": "{p--Brand.Header_End}", "position": 1},
    ]},
}
dump("text.styles.tokens.json", text_styles)
dump("color.styles.tokens.json", color_styles)
dump("effect.styles.tokens.json", effect_styles)

dump("manifest.json", {
    "name": "ARG Design Tokens",
    "collections": {
        "Spacing": {"modes": {"Mode 1": ["Spacing.Mode 1.tokens.json"]}},
        "Typography": {"modes": {"Pretendard": ["Typography.Pretendard.tokens.json"]}},
        "ARG-Color": {"modes": {"Mode 1": ["ARG-Color.Mode 1.tokens.json"]}},
        "Theme": {"modes": {
            "ARG_Lightmode": ["Theme.ARG_Lightmode.tokens.json"],
            "ARG_Darkmode": ["Theme.ARG_Darkmode.tokens.json"],
        }},
    },
    "styles": {
        "text": ["text.styles.tokens.json"],
        "effect": ["effect.styles.tokens.json"],
        "color": ["color.styles.tokens.json"],
    },
})

# ---------- 4. Validate: every reference resolves ----------
def index(*trees):
    idx = {}
    for tr in trees:
        for p, tok in walk(tr):
            idx[".".join(p)] = tok
    return idx

REF = re.compile(r"\{([^{}\"]+)\}")

def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)

problems = []
for mode, th in (("light", light), ("dark", dark)):
    idx = index(prim, th, spacing, typo)
    for name, tr in (("theme", th), ("text", text_styles), ("color", color_styles), ("effect", effect_styles), ("spacing", spacing)):
        for ref in (r for s in strings(tr) for r in REF.findall(s)):
            if ref not in idx:
                problems.append(f"[{mode}/{name}] unresolved {{{ref}}}")
if problems:
    print("\n".join(sorted(set(problems))))
    sys.exit(1)

# ---------- 5. CSS variables (--arg-*) ----------
def slug(parts):
    s = "-".join(parts)
    s = s.replace("%", "pct").replace(",", "-").replace(" ", "-").replace("_", "-")
    s = re.sub(r"^p--", "p-", s)
    s = re.sub(r"-{2,}", "-", s)
    return s.lower()

CSS_PREFIX = {"P1_Basic": "basic", "P2_UI_Color": "ui", "P3_Trading_Color": "trading",
              "P4_Action": "action", "P5_Chart": "chart", "P6_Effect": "effect", "P7_Gradient": "gradient",
              "d--spacing": "space", "d--breakpoints": "bp", "d--borders": "border"}

def var_name(path):
    path = list(path)
    if path[0] in CSS_PREFIX:
        path[0] = CSS_PREFIX[path[0]]
    return "--arg-" + slug(path)

def css_value(v):
    if isinstance(v, str):
        return REF.sub(lambda m: f"var({var_name(m.group(1).split('.'))})", v)
    return v

def decls(tree, indent="  "):
    out = []
    for p, tok in walk(tree):
        v = tok["$value"]
        if tok["$type"] == "string":
            v = f'"{v}", system-ui, sans-serif'
        out.append(f"{indent}{var_name(p)}: {css_value(v)};")
    return out

def shadow(layers):
    return ", ".join(f"{l['offsetX']} {l['offsetY']} {l['blur']} {l['spread']} {css_value(l['color'])}" for l in layers)

def gradient(g):
    stops = ", ".join(f"{css_value(s['color'])} {round(s['position'] * 100, 2):g}%" for s in g["stops"])
    return f"linear-gradient({g['angle']}deg, {stops})"

css = ["/* ARG Design Tokens — generated by build_arg.py, do not edit by hand. */", "",
       "/* Primitives, spacing, typography */", ":root {"]
css += decls(prim) + decls(spacing) + decls(typo)
# Effects and gradients point at theme tokens, so re-resolve them on every themed element
css += ["}", "", ":root, [data-theme] {", "  /* Effects */"]
for name, tok in effect_styles.items():
    css.append(f"  --arg-shadow-{slug([name.removeprefix('eff-')])}: {shadow(tok['$value'])};")
css += ["", "  /* Gradients */"]
for name, tok in color_styles["Gradient"].items():
    css.append(f"  --arg-gradient-{slug([name.split(' - ')[0]])}: {gradient(tok['$value'])};")
css += ["}", "", "/* Theme: ARG_Lightmode (default) */",
        ':root, [data-theme="light"] {', "  color-scheme: light;"] + decls(light) + ["}", "",
        "/* Theme: ARG_Darkmode */", '[data-theme="dark"] {', "  color-scheme: dark;"] + decls(dark) + ["}", "",
        "/* Text styles: .arg-text-<style>-<weight> */"]
for p, tok in walk(text_styles):
    v = tok["$value"]
    cls = "arg-text-" + slug(p[1:])
    css.append(f".{cls} {{ font-family: var(--arg-font-family-family); font-size: {css_value(v['fontSize'])}; "
               f"line-height: {css_value(v['lineHeight'])}; font-weight: {v['fontWeight']}; }}")
(OUT / "arg-tokens.css").write_text("\n".join(css) + "\n", encoding="utf-8")

count = sum(1 for t in (prim, light, spacing, typo, text_styles, color_styles, effect_styles) for _ in walk(t))
print(f"OK — {count} tokens, all references resolve. Output: {OUT}")
print("Agri_Red ramp:", {k: v["$value"] for k, v in prim["p--Primary"]["Agri_Red"].items()})
