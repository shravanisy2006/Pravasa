"""
Pravasa look and feel: styles and small HTML pieces used by app.py.

Design idea: Karnataka's own flag, the Kannada bicolour.
  - Kannada yellow #FFC72C  highlights, badges, the flag band
  - Kannada red    #C8102E  buttons, the wordmark, key numbers
  - Ink            #24201E  text
  - White pages with light photographs of Karnataka behind the top section
Headings use Baloo Tamma 2, a typeface made for Kannada and English together.
The flag band (yellow over red) under the top section is the signature element,
and it matches the Pravasa logo.
"""

import html

STYLE = """
<style>
@font-face {
  font-family: "Baloo Tamma 2"; font-weight: 600; font-display: swap;
  src: url("app/static/BalooTamma2-SemiBold.woff2") format("woff2");
}
@font-face {
  font-family: "Baloo Tamma 2"; font-weight: 800; font-display: swap;
  src: url("app/static/BalooTamma2-ExtraBold.woff2") format("woff2");
}
:root {
  --pv-red: #C8102E;
  --pv-red-dark: #A30D25;
  --pv-yellow: #FFC72C;
  --pv-yellow-soft: #FFF4D1;
  --pv-red-soft: #FBE7EA;
  --pv-ink: #24201E;
  --pv-muted: #6E6862;
  --pv-line: #E9E5DF;
  --pv-display: "Baloo Tamma 2", "Noto Sans Kannada", sans-serif;
}

/* Page frame */
header[data-testid="stHeader"] { background: transparent; }
[data-testid="stMain"] { overflow-x: hidden; }
[data-testid="stMainBlockContainer"] {
  padding-top: 0; padding-bottom: 4rem; max-width: 1120px;
}

/* ---------- Hero: a light photograph of Karnataka behind everything ---------- */
.st-key-hero {
  background:
    linear-gradient(90deg, rgba(255,255,255,.96) 0%, rgba(255,255,255,.88) 48%,
                    rgba(255,255,255,.45) 100%),
    var(--pv-hero-photo, linear-gradient(120deg, #FFF4D1, #FFFFFF)) center / cover no-repeat;
  box-shadow: 0 0 0 100vmax rgba(255,255,255,0);
  width: 100vw !important; max-width: 100vw !important;
  margin-left: calc(50% - 50vw); margin-right: calc(50% - 50vw);
  padding: 2.5rem max(1rem, calc(50vw - 560px)) 3rem;
  box-sizing: border-box;
}
.pv-brandrow { display: flex; align-items: center; gap: .75rem; margin: 0 0 .25rem; }
.pv-brandrow img { width: 64px; height: auto; }
.pv-brand {
  font-family: var(--pv-display) !important; font-weight: 800; font-size: 1.6rem !important;
  color: var(--pv-ink) !important; margin: 0; line-height: 1;
}
.pv-word {
  font-family: var(--pv-display) !important; font-weight: 800;
  font-size: clamp(4rem, 11vw, 7.5rem); line-height: 1; color: var(--pv-red);
  margin: .5rem 0 1rem; padding: 0; letter-spacing: 0;
}
.pv-lede {
  font-size: 1.15rem !important; line-height: 1.6; max-width: 30rem;
  color: var(--pv-ink) !important; margin: 0 0 1.4rem;
}
.pv-points { list-style: none; padding: 0; margin: 0; display: grid; gap: .5rem; }
.pv-points li { font-size: .98rem; padding-left: 1.5rem; position: relative; color: var(--pv-ink); }
.pv-points li::before {
  content: ""; position: absolute; left: 0; top: .35em; width: .8rem; height: .8rem;
  border-radius: 50%;
  background: linear-gradient(var(--pv-yellow) 50%, var(--pv-red) 50%);
}

/* The request panel inside the hero */
.st-key-ask {
  background: #FFFFFF; border-radius: 22px; padding: 1.5rem 1.5rem 1.25rem;
  box-shadow: 0 20px 50px rgba(60, 30, 10, .18);
  border-top: 6px solid var(--pv-yellow);
}
.pv-ask-title {
  font-family: var(--pv-display) !important; font-weight: 800; font-size: 1.6rem !important;
  color: var(--pv-ink) !important; margin: 0 0 .1rem; line-height: 1.2;
}
.pv-ask-sub { color: var(--pv-muted) !important; margin: 0 0 .75rem; font-size: .95rem; }

/* The flag band: Kannada yellow over Kannada red, full width */
.pv-flag {
  height: 20px; width: 100vw; margin: -1rem 0 0 calc(50% - 50vw);
  background: linear-gradient(var(--pv-yellow) 50%, var(--pv-red) 50%);
}

/* ---------- Headings and text ---------- */
.pv-h2 {
  font-family: var(--pv-display) !important; font-weight: 800; font-size: 2.1rem;
  color: var(--pv-ink); margin: 2.25rem 0 .15rem; line-height: 1.15;
}
.pv-h3 {
  font-family: var(--pv-display) !important; font-weight: 800; font-size: 1.45rem !important;
  color: var(--pv-ink); margin: 1.5rem 0 .4rem;
}
.pv-sub { color: var(--pv-muted); margin: 0 0 1rem; font-size: 1rem; }

/* Summary figures: one strip, divided by rules */
.pv-stats {
  display: grid; grid-template-columns: repeat(3, minmax(0, 1fr));
  border-top: 3px solid var(--pv-red); border-bottom: 1px solid var(--pv-line);
  margin: .75rem 0 .5rem;
}
.pv-stat { padding: .9rem 1rem .8rem; border-left: 1px solid var(--pv-line); }
.pv-stat:first-child { border-left: none; padding-left: 0; }
.pv-stat-num {
  font-family: var(--pv-display) !important; font-weight: 800; font-size: 2rem;
  color: var(--pv-ink); line-height: 1.1;
}
.pv-stat:first-child .pv-stat-num { color: var(--pv-red); }
.pv-stat-label { color: var(--pv-muted); font-size: .9rem; }
.pv-budget-ok { color: #1E7A46; font-weight: 700; }
.pv-budget-over { color: var(--pv-red); font-weight: 700; }

/* Trip story */
.st-key-story {
  background: #FFFFFF; border: 1px solid var(--pv-line); border-left: 6px solid var(--pv-yellow);
  border-radius: 4px 18px 18px 4px; padding: 1.25rem 1.5rem 1rem; margin-top: 1rem;
}
.st-key-story p { font-size: 1.05rem; line-height: 1.75; }

/* ---------- Day tabs as pills ---------- */
[data-testid="stTabs"] [role="tablist"] {
  gap: .5rem; flex-wrap: wrap; border-bottom: none; box-shadow: none; margin-bottom: .75rem;
}
[data-testid="stTabs"] [role="tab"] {
  border: 1px solid var(--pv-line); border-radius: 999px; padding: .4rem 1.2rem;
  background: #FFFFFF; height: auto; cursor: pointer;
}
[data-testid="stTabs"] [role="tab"] p {
  font-family: var(--pv-display) !important; font-weight: 600; font-size: 1.05rem !important;
  margin: 0;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
  background: var(--pv-red); border-color: var(--pv-red);
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] p { color: #FFFFFF; }
[data-testid="stTabs"] [role="tab"]:focus-visible { outline: 3px solid var(--pv-yellow); outline-offset: 2px; }
[data-testid="stTabs"] .react-aria-SelectionIndicator { display: none; }

/* Route map frame */
[data-testid="stIFrame"] iframe, iframe[title="st.iframe"] {
  border-radius: 18px; border: 1px solid var(--pv-line);
}

/* Each place in a day */
[class*="st-key-place_"] {
  background: #FFFFFF; border: 1px solid var(--pv-line); border-radius: 20px;
  padding: 1.25rem 1.4rem 1rem; margin-top: .9rem;
  box-shadow: 0 6px 18px rgba(60, 30, 10, .05);
}
.pv-stop { color: var(--pv-muted); font-size: .9rem; margin: 0; }
.pv-place {
  font-family: var(--pv-display) !important; font-weight: 800; font-size: 1.7rem !important;
  color: var(--pv-ink); line-height: 1.15; margin: .1rem 0 0;
}
.pv-place-kn {
  font-family: var(--pv-display) !important; font-weight: 600; font-size: 1.1rem !important;
  color: var(--pv-red); margin: 0 0 .6rem;
}
.pv-district {
  font-family: "Noto Sans", "Noto Sans Kannada", sans-serif !important; font-weight: 400;
  font-size: .9rem; color: var(--pv-muted); margin-left: .6rem;
}
.pv-famous { font-size: 1rem; line-height: 1.6; margin: 0 0 .5rem; }
.pv-wiki { color: var(--pv-muted); font-size: .92rem; line-height: 1.6; margin: 0 0 .25rem; }
.pv-travel {
  display: inline-block; font-size: .9rem; color: var(--pv-ink);
  background: var(--pv-yellow-soft); border-radius: 999px; padding: .15rem .75rem; margin: .1rem 0 .5rem;
}
.pv-travel.long { color: var(--pv-red-dark); background: var(--pv-red-soft); }
.pv-facts {
  margin-left: 0 !important; padding-left: 0 !important;
  display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: .6rem 1.25rem; margin: .9rem 0 .4rem; padding: .8rem 0 0;
  border-top: 1px dashed var(--pv-line);
}
.pv-fact { margin: 0; padding: 0; }
.pv-fact dt { color: var(--pv-muted); font-size: .8rem; }
.pv-fact dd { margin: 0; font-size: .95rem; font-weight: 700; color: var(--pv-ink); }

/* ---------- Photo gallery: swipe, scroll, or use the arrows ---------- */
.pvg { position: relative; }
.pvg > input { position: absolute; opacity: 0; pointer-events: none; }
.pvg-view { overflow: hidden; border-radius: 14px; background: #F2EFEA; aspect-ratio: 4 / 3; }
.pvg-track { display: flex; height: 100%; transition: transform .35s ease; }
.pvg-track figure { flex: 0 0 100%; margin: 0; height: 100%; position: relative; }
.pvg-track img { width: 100%; height: 100%; object-fit: cover; display: block; }
.pvg-track figcaption {
  position: absolute; left: 0; right: 0; bottom: 0; padding: 1.2rem .6rem .35rem;
  font-size: .7rem; color: #FFFFFF; background: linear-gradient(transparent, rgba(0,0,0,.55));
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.pvg-track figcaption a { color: #FFFFFF; }
.pvg-nav { display: flex; align-items: center; justify-content: space-between; margin-top: .45rem; }
.pvg-step { display: none; align-items: center; justify-content: space-between; width: 100%; }
.pvg-step label {
  width: 2.2rem; height: 2.2rem; border-radius: 50%; display: grid; place-items: center;
  border: 1px solid var(--pv-line); background: #FFFFFF; cursor: pointer;
  font-size: 1.2rem; line-height: 1; color: var(--pv-ink); user-select: none;
}
.pvg-step label:hover { border-color: var(--pv-red); color: var(--pv-red); }
.pvg-step label.off { visibility: hidden; }
.pvg-count { font-size: .85rem; color: var(--pv-muted); }
.pvg > input:focus-visible ~ .pvg-view { outline: 3px solid var(--pv-yellow); outline-offset: 2px; }
.pvg-empty {
  aspect-ratio: 4 / 3; border-radius: 14px; display: grid; place-items: center;
  background: linear-gradient(var(--pv-yellow-soft) 50%, var(--pv-red-soft) 50%);
  color: var(--pv-muted); font-size: .9rem;
}

/* ---------- What travellers say ---------- */
.pv-says {
  margin: .9rem 0 .3rem; padding: .9rem 1rem .8rem 1rem; border-radius: 14px;
  background: #FAF8F5; border: 1px solid var(--pv-line);
}
.pv-says-title {
  font-family: var(--pv-display) !important; font-weight: 800; font-size: 1.1rem !important;
  margin: 0 0 .25rem; color: var(--pv-ink);
}
.pv-says blockquote {
  margin: 0; padding: 0 0 0 .9rem; border-left: 3px solid var(--pv-red);
  font-size: .95rem; line-height: 1.6; color: var(--pv-ink);
}
.pv-says-src { margin: .4rem 0 0; font-size: .8rem; color: var(--pv-muted); }

/* Where to stay tonight */
[class*="st-key-night_"] {
  background: var(--pv-yellow-soft); border-radius: 20px; padding: 1.1rem 1.4rem;
  margin-top: 1.1rem;
}
.pv-hotel { margin: .35rem 0; }

/* Links */
.pv-wiki a, .pv-hotel a, .pv-foot a, .pv-says a { color: var(--pv-red-dark); font-weight: 700; }

/* Buttons */
.stButton button[kind="primary"], .stDownloadButton button[kind="primary"] {
  font-weight: 700; padding: .55rem 1.4rem; color: #FFFFFF;
}
.stButton button[kind="primary"] p, .stDownloadButton button[kind="primary"] p {
  color: #FFFFFF !important; font-weight: 700;
}

/* Emergency numbers */
.pv-help { list-style: none; margin: 0; padding: 0; }
.pv-help li {
  display: flex; justify-content: space-between; gap: 1rem; align-items: baseline;
  padding: .55rem 0; border-bottom: 1px solid var(--pv-line);
}
.pv-help span { color: var(--pv-ink); }
.pv-help a {
  font-family: var(--pv-display) !important; font-weight: 800; font-size: 1.2rem;
  color: var(--pv-red); text-decoration: none; white-space: nowrap;
}

/* Footer */
.pv-foot {
  margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--pv-line);
  color: var(--pv-muted); font-size: .85rem;
}

@media (prefers-reduced-motion: reduce) { .pvg-track { transition: none; } }
@media (max-width: 640px) {
  .st-key-hero {
    padding: 1.75rem 1rem 2rem;
    background:
      linear-gradient(rgba(255,255,255,.9), rgba(255,255,255,.9)),
      var(--pv-hero-photo, linear-gradient(120deg, #FFF4D1, #FFFFFF)) center / cover no-repeat;
  }
  .pv-stats { grid-template-columns: 1fr; }
  .pv-stat { border-left: none; padding-left: 0; border-top: 1px solid var(--pv-line); }
  .pv-stat:first-child { border-top: none; }
  .pv-h2 { font-size: 1.7rem; }
}
</style>
"""

e = html.escape  # makes text safe to put inside HTML


def hero_photo_style(photo_url):
    """Put a light photo behind the top section (or a soft colour if none)."""
    if not photo_url:
        return ""
    return f"<style>:root {{ --pv-hero-photo: url('{e(photo_url)}'); }}</style>"


def hero_intro(place_count):
    return f"""
<div class="pv-brandrow"><img src="app/static/logo.png" alt="Pravasa logo">
<p class="pv-brand">Pravasa</p></div>
<h1 class="pv-word">ಪ್ರವಾಸ</h1>
<p class="pv-lede">Say where you'd like to go, in ಕನ್ನಡ or English. Pravasa plans the days,
the roads and the stays across Karnataka.</p>
<ul class="pv-points">
  <li>{place_count} hand-checked places, from Hampi to the coast</li>
  <li>Real road distances, weather and season advice</li>
  <li>Speaks and listens in Kannada</li>
</ul>
"""


def flag_band():
    return '<div class="pv-flag" role="presentation"></div>'


def section_title(title, sub=None):
    out = f'<h2 class="pv-h2">{e(title)}</h2>'
    if sub:
        out += f'<p class="pv-sub">{e(sub)}</p>'
    return out


def stats_strip(cost, budget, km):
    diff = budget - cost
    status = (f'<span class="pv-budget-ok">₹{diff:,} under budget</span>' if diff >= 0
              else f'<span class="pv-budget-over">₹{-diff:,} over budget</span>')
    return f"""
<div class="pv-stats">
  <div class="pv-stat"><div class="pv-stat-num">₹{cost:,}</div>
    <div class="pv-stat-label">Estimated total</div></div>
  <div class="pv-stat"><div class="pv-stat-num">₹{budget:,}</div>
    <div class="pv-stat-label">Your budget, {status}</div></div>
  <div class="pv-stat"><div class="pv-stat-num">{km:,} km</div>
    <div class="pv-stat-label">Total driving, including the way home</div></div>
</div>
"""


def place_header(n, place, travel_text, long_day):
    cls = "pv-travel long" if long_day else "pv-travel"
    return f"""
<p class="pv-stop">Stop {n}</p>
<p class="pv-place">{e(place['name'])}</p>
<p class="pv-place-kn">{e(place['name_kn'])}<span class="pv-district">{e(place['district'])}</span></p>
<span class="{cls}">{e(travel_text)}</span>
<p class="pv-famous">{e(place['famous_for'])}</p>
"""


def wiki_text(summary, url):
    return (f'<p class="pv-wiki">{e(summary)} <a href="{e(url)}" target="_blank">'
            f'Read more on Wikipedia</a></p>')


def gallery(gid, photos, name):
    """A photo carousel that works without JavaScript: arrows, swipe-free, keyboard."""
    if not photos:
        return f'<div class="pvg-empty">Photos of {e(name)} will appear here</div>'
    n = len(photos)
    radios = "".join(
        f'<input type="radio" name="{gid}" id="{gid}-{i}" aria-label="Photo {i + 1} of {n}"'
        f'{" checked" if i == 0 else ""}>' for i in range(n))
    figures = "".join(
        f'<figure><img src="{e(p["url"])}" alt="{e(name)}, photo {i + 1}" loading="lazy">'
        f'<figcaption><a href="{e(p["page"])}" target="_blank">{e(p["credit"] or "Wikimedia Commons")}'
        f'</a></figcaption></figure>' for i, p in enumerate(photos))
    steps = ""
    for i in range(n):
        prev_cls = ' class="off"' if i == 0 else ""
        next_cls = ' class="off"' if i == n - 1 else ""
        steps += (f'<div class="pvg-step pvg-step-{i}">'
                  f'<label for="{gid}-{max(i - 1, 0)}"{prev_cls} title="Previous photo">‹</label>'
                  f'<span class="pvg-count">{i + 1} / {n}</span>'
                  f'<label for="{gid}-{min(i + 1, n - 1)}"{next_cls} title="Next photo">›</label></div>')
    rules = "".join(
        f"#{gid}-{i}:checked ~ .pvg-view .pvg-track {{ transform: translateX(-{i * 100}%); }}"
        f"#{gid}-{i}:checked ~ .pvg-nav .pvg-step-{i} {{ display: flex; }}" for i in range(n))
    return (f'<div class="pvg">{radios}<div class="pvg-view"><div class="pvg-track">{figures}'
            f'</div></div><div class="pvg-nav">{steps}</div><style>{rules}</style></div>')


def travellers_say(notes):
    """Traveller-written notes from Wikivoyage."""
    return (f'<div class="pv-says"><p class="pv-says-title">What travellers say</p>'
            f'<blockquote>{e(notes["text"])}</blockquote>'
            f'<p class="pv-says-src">From the Wikivoyage traveller guide to '
            f'<a href="{e(notes["url"])}" target="_blank">{e(notes["title"])}</a>, '
            f'written by travellers</p></div>')


def facts(place, fee_text):
    items = [
        ("Time to spend", f"About {place['visit_hours']} hours"),
        ("Entry", fee_text),
        ("Open", place["timings"]),
        ("Local food to try", place["local_food"]),
    ]
    cells = "".join(f'<div class="pv-fact"><dt>{e(k)}</dt><dd>{e(str(v))}</dd></div>'
                    for k, v in items)
    return f'<dl class="pv-facts">{cells}</dl>'


def hotel_line(h):
    bits = [e(h["type"]), f"{h['km']} km away"]
    if h.get("stars"):
        bits.append(f"{e(str(h['stars']))}★")
    if h.get("phone"):
        bits.append(f'<a href="tel:{e(h["phone"])}">{e(h["phone"])}</a>')
    bits.append(f'<a href="{e(h["maps"])}" target="_blank">map</a>')
    return f'<p class="pv-hotel"><b>{e(h["name"])}</b><br>{", ".join(bits)}</p>'


def helplines(items):
    rows = "".join(
        f'<li><span>{e(label.split(" ", 1)[1])}</span>'
        f'<a href="tel:{e(number.split(" /")[0].replace("-", ""))}">{e(number)}</a></li>'
        for label, number in items)
    return f'<ul class="pv-help">{rows}</ul>'


def footer():
    return ('<p class="pv-foot">Pravasa plans with data from OpenStreetMap, OSRM, Wikipedia '
            'and Open-Meteo. Costs, fees and timings are estimates; please confirm '
            'locally before you travel.</p>')