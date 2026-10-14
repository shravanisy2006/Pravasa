"""
Pravasa PDF itinerary.

Builds a printable PDF of the trip with fpdf2. Kannada text needs a font
that has Kannada letters and "text shaping" (so letters join correctly),
so the Noto Sans fonts in the fonts/ folder are used for both languages.
"""

from pathlib import Path

from fpdf import FPDF

from weather import HELPLINES, weather_text

FONTS = Path(__file__).parent / "fonts"


class TripPDF(FPDF):
    def footer(self):
        self.set_y(-12)
        self.set_font("Noto", size=8)
        self.set_text_color(130)
        self.cell(0, 6, f"Pravasa · Karnataka AI Travel Planner · page {self.page_no()}",
                  align="C")


def _setup():
    pdf = TripPDF(format="A4")
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(True, margin=18)
    pdf.add_font("Noto", "", FONTS / "NotoSans-Regular.ttf")
    pdf.add_font("Noto", "B", FONTS / "NotoSans-Bold.ttf")
    pdf.add_font("NotoKn", "", FONTS / "NotoSansKannada-Regular.ttf")
    pdf.add_font("NotoKn", "B", FONTS / "NotoSansKannada-Bold.ttf")
    pdf.set_fallback_fonts(["NotoKn"])   # Kannada letters use the Kannada font
    pdf.set_text_shaping(True)           # join Kannada letters correctly
    return pdf


def _heading(pdf, text, size=13):
    pdf.ln(2)
    pdf.set_font("Noto", "B", size)
    pdf.set_text_color(20, 60, 120)
    pdf.multi_cell(0, 7, text, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0)


def _para(pdf, text, size=10, bold=False):
    pdf.set_font("Noto", "B" if bold else "", size)
    pdf.multi_cell(0, 5.5, text, new_x="LMARGIN", new_y="NEXT")


def build_pdf(result, info, story=None, weather=None, hotels=None):
    """Return the itinerary as PDF bytes."""
    pdf = _setup()
    pdf.add_page()
    costs = result["costs"]

    pdf.set_font("Noto", "B", 20)
    pdf.cell(0, 10, "Pravasa · ಪ್ರವಾಸ", new_x="LMARGIN", new_y="NEXT")
    _para(pdf, f"Your {info['days']}-day Karnataka trip from {info['start_city']}", 12, bold=True)
    _para(pdf, f"Estimated cost: ₹{costs['Total']:,}  ·  Budget: ₹{info['budget']:,}  ·  "
               f"Distance: {result['total_km']:,} km  ·  Travel: {info['transport']}  ·  "
               f"Stay: {info['stay_style']}")

    if story:
        _heading(pdf, "Your trip, in short")
        _para(pdf, story.replace("**", "").replace("#", ""))

    for i, day in enumerate(result["days"]):
        _heading(pdf, f"Day {day['day']}")
        w = weather[i] if weather and i < len(weather) else None
        if w:
            # emojis don't print in PDF fonts, so drop the icon
            _para(pdf, "Weather: " + weather_text(w).split(" ", 1)[1], 9)
        if not day["stops"]:
            _para(pdf, "A free day to relax.")
        for n, stop in enumerate(day["stops"], start=1):
            p = stop["place"]
            pdf.ln(1)
            _para(pdf, f"{n}. {p['name']}  ({p['name_kn']})", 11, bold=True)
            fee = p.get("entry_fee_inr_approx")
            fee_text = "Free" if fee == 0 else (f"about ₹{fee}" if fee else p.get("fee_note", "Check locally"))
            _para(pdf, f"{stop['travel_km']} km, about {stop['travel_hours']} h to get here  ·  "
                       f"Spend about {p['visit_hours']} h  ·  Entry: {fee_text}", 9)
            _para(pdf, f"Famous for: {p['famous_for']}", 9)
            _para(pdf, f"Timings: {p['timings']}  ·  Try: {p['local_food']}", 9)
        night = hotels.get(day["day"]) if hotels else None
        if night:
            names = "; ".join(f"{h['name']} ({h['type']})" for h in night)
            _para(pdf, f"Stay tonight (suggestions, check before booking): {names}", 9)

    _heading(pdf, "Approximate costs")
    for k, v in costs.items():
        _para(pdf, f"{k}: ₹{v:,}", 10, bold=(k == "Total"))

    _heading(pdf, "Emergency & helpline numbers")
    for label, number in HELPLINES:
        _para(pdf, f"{label.split(' ', 1)[1]}: {number}", 10)

    pdf.ln(3)
    _para(pdf, "Costs, timings and fees are estimates. Please confirm locally before travelling.", 8)
    return bytes(pdf.output())