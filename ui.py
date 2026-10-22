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

from i18n import (HELPLINE_KN, SEASON_ROWS, WORDS_KN, is_kn, lang, month_short, pf,
                  t, w)

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
[data-testid="stMain"] { overflow-x: hidden; }
[data-testid="stMainBlockContainer"] {
  padding-top: 3.75rem; padding-bottom: 4rem; max-width: 1120px;
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
  font-family: var(--pv-display) !important; font-weight: 600; font-size: 1.15rem !important;
  color: var(--pv-red) !important; margin: 0; line-height: 1.2;
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
.pv-help { list-style: none; margin: 0 !important; padding: 0 !important; }
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


/* ---------- Top menu bar ---------- */
header[data-testid="stHeader"] {
  background: rgba(255,255,255,.96); border-bottom: 1px solid var(--pv-line);
  backdrop-filter: blur(6px);
}
[data-testid="stHeader"] img[data-testid="stHeaderLogo"], [data-testid="stLogo"] { height: 2.6rem; }
[data-testid="stTopNavLink"] p, [data-testid="stNavSectionHeader"] p,
header [data-testid="stPageLink-NavLink"] p { font-weight: 600; }
[data-testid="stTopNavLink"][aria-current="page"], header a[aria-current="page"] {
  box-shadow: inset 0 -3px 0 var(--pv-red);
}

/* ---------- Page banner (every page except Home) ---------- */
.st-key-banner {
  background:
    linear-gradient(90deg, rgba(255,255,255,.95) 0%, rgba(255,255,255,.86) 55%,
                    rgba(255,255,255,.55) 100%),
    var(--pv-hero-photo, linear-gradient(120deg, #FFF4D1, #FFFFFF)) center 40% / cover no-repeat;
  width: 100vw !important; max-width: 100vw !important;
  margin-left: calc(50% - 50vw); margin-right: calc(50% - 50vw);
  padding: 2.25rem max(1rem, calc(50vw - 560px)) 2rem;
  box-sizing: border-box;
}
.pv-banner-title {
  font-family: var(--pv-display) !important; font-weight: 800;
  font-size: clamp(2.2rem, 5vw, 3.2rem) !important; line-height: 1.1;
  color: var(--pv-ink) !important; margin: 0 0 .35rem;
}
.pv-banner-sub { font-size: 1.1rem !important; color: var(--pv-ink) !important; margin: 0; max-width: 42rem; }

/* ---------- Theme tiles on Home ---------- */
[class*="st-key-tile_"] {
  background: #FFFFFF; border: 1px solid var(--pv-line); border-radius: 20px;
  overflow: hidden; padding: 0 0 .6rem;
}
[class*="st-key-tile_"] [data-testid="stPageLink"] { padding: 0 1rem; }
.pv-tile-img {
  aspect-ratio: 16 / 10; background-size: cover; background-position: center;
  background-color: var(--pv-yellow-soft); position: relative;
}
.pv-tile-img::after {
  content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 6px;
  background: linear-gradient(90deg, var(--pv-yellow) 50%, var(--pv-red) 50%);
}
.pv-tile-body { padding: .8rem 1rem 0; }
.pv-tile-name {
  font-family: var(--pv-display) !important; font-weight: 800; font-size: 1.45rem !important;
  margin: 0; color: var(--pv-ink); line-height: 1.1;
}
.pv-tile-kn {
  font-family: var(--pv-display) !important; font-weight: 600; font-size: 1.05rem !important;
  color: var(--pv-red); margin: 0;
}

/* ---------- How it works ---------- */
.pv-steps { list-style: none; margin: .5rem 0 0 !important; padding: 0 !important; display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1.25rem; counter-reset: step; }
.pv-steps li { counter-increment: step; padding: 1.1rem 1.2rem; border-radius: 18px;
  background: #FAF8F5; border: 1px solid var(--pv-line); }
.pv-steps li::before {
  content: counter(step); display: grid; place-items: center; width: 2.2rem; height: 2.2rem;
  border-radius: 50%; background: var(--pv-red); color: #FFFFFF; margin-bottom: .6rem;
  font-family: var(--pv-display); font-weight: 800; font-size: 1.15rem;
}
.pv-steps b { display: block; font-family: var(--pv-display); font-size: 1.2rem; margin-bottom: .2rem; }
.pv-steps span { color: var(--pv-muted); font-size: .95rem; line-height: 1.55; }

/* ---------- Explore cards ---------- */
[class*="st-key-card_"] {
  background: #FFFFFF; border: 1px solid var(--pv-line); border-radius: 20px;
  overflow: hidden; padding: 0 1rem 1rem; height: 100%;
}
.pv-card-img {
  aspect-ratio: 4 / 3; margin: 0 -1rem .8rem; background-size: cover; background-position: center;
  background-color: var(--pv-yellow-soft);
}
.pv-card-img.none {
  display: grid; place-items: center; color: var(--pv-muted); font-size: .9rem;
  background: linear-gradient(var(--pv-yellow-soft) 50%, var(--pv-red-soft) 50%);
}
.pv-card-name {
  font-family: var(--pv-display) !important; font-weight: 800; font-size: 1.3rem !important;
  margin: 0; color: var(--pv-ink); line-height: 1.15;
}
.pv-card-kn {
  font-family: var(--pv-display) !important; font-weight: 600; font-size: 1rem !important;
  color: var(--pv-red); margin: 0 0 .35rem;
}
.pv-card-meta { color: var(--pv-muted); font-size: .85rem; margin: 0 0 .5rem; }
.pv-card-text { font-size: .93rem; line-height: 1.55; margin: 0 0 .6rem; }
.pv-chips { display: flex; flex-wrap: wrap; gap: .35rem; margin: 0 0 .7rem; }
.pv-chip { font-size: .78rem; padding: .1rem .6rem; border-radius: 999px;
  background: var(--pv-yellow-soft); color: var(--pv-ink); }

/* ---------- Panels on Plan / My trip / Help ---------- */
.st-key-planform, .st-key-empty, .st-key-helpbox, .st-key-filters,
.st-key-seasonbox, .st-key-aboutbox, .st-key-sourcebox {
  background: #FFFFFF; border: 1px solid var(--pv-line); border-radius: 20px;
  padding: 1.4rem 1.5rem; margin-top: 1.25rem;
  box-shadow: 0 6px 18px rgba(60, 30, 10, .05);
}

/* Season guide */
.pv-season { width: 100%; border-collapse: collapse; font-size: .93rem; }
.pv-season th { text-align: left; font-weight: 700; padding: .5rem .5rem; border-bottom: 2px solid var(--pv-red); }
.pv-season td { padding: .55rem .5rem; border-bottom: 1px solid var(--pv-line); vertical-align: top; }
.pv-season td:first-child { font-weight: 700; }
.pv-good { background: var(--pv-yellow-soft); }


/* ---------- Light photo behind a section ---------- */
[class*="st-key-photo_"] {
  background:
    linear-gradient(rgba(255,255,255,.88), rgba(255,255,255,.92)),
    var(--pv-sec-photo, linear-gradient(#FFFFFF, #FFFFFF)) center / cover no-repeat;
  width: 100vw !important; max-width: 100vw !important;
  margin: -1rem calc(50% - 50vw) 0; box-sizing: border-box;
  padding: 1rem max(1rem, calc(50vw - 560px)) 2.5rem;
  border-bottom: 1px solid var(--pv-line);
}
/* Sections further down the page get breathing room above them */
.st-key-photo_how, .st-key-photo_costs {
  margin-top: 2.5rem !important; border-top: 1px solid var(--pv-line);
}
[class*="st-key-photo_"] .pv-h2 { margin-top: 1.25rem; }

/* ---------- ಕನ್ನಡ / English switch ---------- */
.st-key-langbar { align-items: flex-end; }
.st-key-langbar [data-testid="stButtonGroup"] { justify-content: flex-end; }


/* ---------- Loading card (yellow-to-red bar, like the flag) ---------- */
.pv-loader {
  margin: 1.5rem auto; max-width: 560px; background: #FFFFFF; text-align: left;
  border: 1px solid var(--pv-line); border-radius: 20px; padding: 1.3rem 1.5rem 1.4rem;
  box-shadow: 0 12px 30px rgba(60, 30, 10, .10);
}
.pv-loader-title {
  font-family: var(--pv-display) !important; font-weight: 800; font-size: 1.35rem !important;
  color: var(--pv-ink); margin: 0;
}
.pv-loader-sub { color: var(--pv-muted); font-size: .95rem; margin: .15rem 0 0; }
.pv-loader-bar {
  height: 8px; border-radius: 999px; background: var(--pv-yellow-soft);
  overflow: hidden; margin-top: 1rem; position: relative;
}
.pv-loader-bar::after {
  content: ""; position: absolute; top: 0; bottom: 0; left: 0; width: 40%;
  border-radius: 999px; background: linear-gradient(90deg, var(--pv-yellow), var(--pv-red));
  animation: pv-slide 1.2s ease-in-out infinite;
}
@keyframes pv-slide { from { transform: translateX(-100%); } to { transform: translateX(260%); } }

/* ---------- One-tap example chips ---------- */
.pv-try { font-size: .85rem; color: var(--pv-muted); margin: .4rem 0 .1rem; }
[class*="st-key-ex_"] button {
  border-radius: 999px; padding: .2rem .85rem; min-height: 0;
  background: var(--pv-yellow-soft); border: 1px solid #F3DE9A;
}
[class*="st-key-ex_"] button p { font-size: .85rem; }
[class*="st-key-ex_"] button:hover { border-color: var(--pv-red); color: var(--pv-red); }

@media (prefers-reduced-motion: reduce) {
  .pvg-track { transition: none; }
  .pv-loader-bar::after { animation: none; width: 100%; }
}
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
  .pv-steps { grid-template-columns: 1fr; }
  .st-key-banner { padding: 1.5rem 1rem; }
}
</style>
"""

e = html.escape  # makes text safe to put inside HTML


def hero_photo_style(photo_url):
    """Put a light photo behind the top section (or a soft colour if none)."""
    if not photo_url:
        return ""
    return f"<style>:root {{ --pv-hero-photo: url('{e(photo_url)}'); }}</style>"


def section_photo_style(key, photo_url):
    """A light photo behind one section (the container with this key)."""
    if not photo_url:
        return ""
    return f"<style>.st-key-{key} {{ --pv-sec-photo: url('{e(photo_url)}'); }}</style>"


def hero_intro(place_count):
    return f"""
<p class="pv-brand">{"ಕರ್ನಾಟಕ ಪ್ರವಾಸ ಯೋಜಕ" if is_kn() else "Pravasa · Karnataka trip planner"}</p>
<h1 class="pv-word">ಪ್ರವಾಸ</h1>
<p class="pv-lede">{e(t("lede"))}</p>
<ul class="pv-points">
  <li>{e(t("point1", n=place_count))}</li>
  <li>{e(t("point2"))}</li>
  <li>{e(t("point3"))}</li>
</ul>
"""


def loader(title, sub=""):
    sub_html = f'<p class="pv-loader-sub">{e(sub)}</p>' if sub else ""
    return (f'<div class="pv-loader" role="status"><p class="pv-loader-title">{e(title)}</p>'
            f'{sub_html}<div class="pv-loader-bar"></div></div>')


def flag_band():
    return '<div class="pv-flag" role="presentation"></div>'


def section_title(title, sub=None):
    out = f'<h2 class="pv-h2">{e(title)}</h2>'
    if sub:
        out += f'<p class="pv-sub">{e(sub)}</p>'
    return out


def banner(title, sub=None):
    out = f'<p class="pv-banner-title">{e(title)}</p>'
    if sub:
        out += f'<p class="pv-banner-sub">{e(sub)}</p>'
    return out


def stats_strip(cost, budget, km):
    diff = budget - cost
    status = (f'<span class="pv-budget-ok">{e(t("under", x=f"{diff:,}"))}</span>' if diff >= 0
              else f'<span class="pv-budget-over">{e(t("over", x=f"{-diff:,}"))}</span>')
    unit = "ಕಿ.ಮೀ" if is_kn() else "km"
    return f"""
<div class="pv-stats">
  <div class="pv-stat"><div class="pv-stat-num">₹{cost:,}</div>
    <div class="pv-stat-label">{e(t("est_total"))}</div></div>
  <div class="pv-stat"><div class="pv-stat-num">₹{budget:,}</div>
    <div class="pv-stat-label">{e(t("your_budget"))}, {status}</div></div>
  <div class="pv-stat"><div class="pv-stat-num">{km:,} {unit}</div>
    <div class="pv-stat-label">{e(t("total_drive"))}</div></div>
</div>
"""


def _names(place):
    """(main name, second name): Kannada first when the site is in Kannada."""
    if is_kn():
        return place["name_kn"], place["name"]
    return place["name"], place["name_kn"]


def place_header(n, place, travel_text, long_day):
    cls = "pv-travel long" if long_day else "pv-travel"
    main, second = _names(place)
    return f"""
<p class="pv-stop">{e(t("stop_n", n=n))}</p>
<p class="pv-place">{e(main)}</p>
<p class="pv-place-kn">{e(second)}<span class="pv-district">{e(w(place['district']))}</span></p>
<span class="{cls}">{e(travel_text)}</span>
<p class="pv-famous">{e(pf(place, 'famous_for'))}</p>
"""


def wiki_text(summary, url, in_english=False):
    note = t("english_note") if in_english else ""
    return (f'<p class="pv-wiki">{e(summary)} <a href="{e(url)}" target="_blank">'
            f'{e(t("read_more_wiki") + note)}</a></p>')


def gallery(gid, photos, name):
    """A photo carousel that works without JavaScript: arrows and keyboard."""
    if not photos:
        return f'<div class="pvg-empty">{e(t("photos_soon", name=name))}</div>'
    n = len(photos)
    radios = "".join(
        f'<input type="radio" name="{gid}" id="{gid}-{i}" '
        f'aria-label="{e(t("photo_n", i=i + 1, n=n))}"{" checked" if i == 0 else ""}>'
        for i in range(n))
    figures = "".join(
        f'<figure><img src="{e(p["url"])}" alt="{e(name)}, {i + 1}" loading="lazy">'
        f'<figcaption><a href="{e(p["page"])}" target="_blank">{e(p["credit"] or "Wikimedia Commons")}'
        f'</a></figcaption></figure>' for i, p in enumerate(photos))
    steps = ""
    for i in range(n):
        prev_cls = ' class="off"' if i == 0 else ""
        next_cls = ' class="off"' if i == n - 1 else ""
        steps += (f'<div class="pvg-step pvg-step-{i}">'
                  f'<label for="{gid}-{max(i - 1, 0)}"{prev_cls} title="{e(t("prev_photo"))}">‹</label>'
                  f'<span class="pvg-count">{i + 1} / {n}</span>'
                  f'<label for="{gid}-{min(i + 1, n - 1)}"{next_cls} title="{e(t("next_photo"))}">›</label></div>')
    rules = "".join(
        f"#{gid}-{i}:checked ~ .pvg-view .pvg-track {{ transform: translateX(-{i * 100}%); }}"
        f"#{gid}-{i}:checked ~ .pvg-nav .pvg-step-{i} {{ display: flex; }}" for i in range(n))
    return (f'<div class="pvg">{radios}<div class="pvg-view"><div class="pvg-track">{figures}'
            f'</div></div><div class="pvg-nav">{steps}</div><style>{rules}</style></div>')


def travellers_say(notes):
    """Traveller-written notes from Wikivoyage."""
    link = f'<a href="{e(notes["url"])}" target="_blank">{e(notes["title"])}</a>'
    source = e(t("travellers_src", link="@@LINK@@")).replace("@@LINK@@", link)
    return (f'<div class="pv-says"><p class="pv-says-title">{e(t("travellers_say"))}</p>'
            f'<blockquote>{e(notes["text"])}</blockquote>'
            f'<p class="pv-says-src">{source}</p></div>')


def facts(place, fee_text):
    items = [
        (t("fact_time"), t("about_hours", h=place["visit_hours"])),
        (t("fact_entry"), fee_text),
        (t("fact_open"), place["timings"]),
        (t("fact_food"), pf(place, "local_food")),
    ]
    cells = "".join(f'<div class="pv-fact"><dt>{e(k)}</dt><dd>{e(str(v))}</dd></div>'
                    for k, v in items)
    return f'<dl class="pv-facts">{cells}</dl>'


def hotel_line(h):
    bits = [e(w(h["type"])), e(t("km_away", km=h["km"]))]
    if h.get("stars"):
        bits.append(f"{e(str(h['stars']))}★")
    if h.get("phone"):
        bits.append(f'<a href="tel:{e(h["phone"])}">{e(h["phone"])}</a>')
    bits.append(f'<a href="{e(h["maps"])}" target="_blank">{e(t("map"))}</a>')
    return f'<p class="pv-hotel"><b>{e(h["name"])}</b><br>{", ".join(bits)}</p>'


def helplines(items):
    rows = ""
    for label, number in items:
        label = HELPLINE_KN.get(label, label) if is_kn() else label
        rows += (f'<li><span>{e(label.split(" ", 1)[1])}</span>'
                 f'<a href="tel:{e(number.split(" /")[0].replace("-", ""))}">{e(number)}</a></li>')
    return f'<ul class="pv-help">{rows}</ul>'


def footer():
    return f'<p class="pv-foot">{e(t("footer"))}</p>'


def theme_tile(theme, count, image):
    style = f' style="background-image:url(\'{e(image)}\')"' if image else ""
    main, second = (WORDS_KN[theme], theme) if is_kn() else (theme, WORDS_KN[theme])
    return (f'<div class="pv-tile-img"{style} role="img" aria-label="{e(theme)}"></div>'
            f'<div class="pv-tile-body"><p class="pv-tile-name">{e(main)}</p>'
            f'<p class="pv-tile-kn">{e(second)}</p></div>')


def how_it_works():
    steps = [(t("step1_t"), t("step1_d")), (t("step2_t"), t("step2_d")),
             (t("step3_t"), t("step3_d"))]
    items = "".join(f"<li><b>{e(a)}</b><span>{e(b)}</span></li>" for a, b in steps)
    return f'<ol class="pv-steps">{items}</ol>'


def place_card(place, image):
    if image:
        img = (f'<div class="pv-card-img" style="background-image:url(\'{e(image)}\')" '
               f'role="img" aria-label="{e(place["name"])}"></div>')
    else:
        img = f'<div class="pv-card-img none">{e(t("no_photo"))}</div>'
    main, second = _names(place)
    months = ", ".join(month_short(m) for m in sorted(place["best_months"],
                                                       key=lambda m: (m - 6) % 12))
    chips = "".join(f'<span class="pv-chip">{e(w(c))}</span>' for c in place["categories"])
    return (f'{img}<p class="pv-card-name">{e(main)}</p>'
            f'<p class="pv-card-kn">{e(second)}</p>'
            f'<p class="pv-card-meta">{e(t("card_meta", district=w(place["district"]), months=months))}</p>'
            f'<div class="pv-chips">{chips}</div>'
            f'<p class="pv-card-text">{e(pf(place, "famous_for"))}</p>')


def season_guide():
    rows = SEASON_ROWS[lang()]
    body = "".join(f'<tr><td>{e(a)}</td><td class="pv-good">{e(b)}</td><td>{e(c)}</td></tr>'
                   for a, b, c in rows)
    return (f'<table class="pv-season"><thead><tr><th>{e(t("th_area"))}</th>'
            f'<th>{e(t("th_best"))}</th><th>{e(t("th_mind"))}</th></tr></thead>'
            f'<tbody>{body}</tbody></table>')
