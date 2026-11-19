"""Makes PDF downloads (Phase 9)."""
import re
from fpdf import FPDF

DISCLAIMER = ("Educational demo only. This is not medical advice. "
              "Please talk to a doctor or dietitian.")


def _clean(text):
    text = re.sub(r"[*#`_]", "", str(text))
    text = text.replace("\u2022", "-").replace("\u2019", "'").replace("\u2013", "-")
    return text.encode("latin-1", "replace").decode("latin-1")


def make_pdf(title, sections):
    """sections = list of (heading, text). Returns PDF as bytes."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 10, _clean(title), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    for heading, text in sections:
        pdf.set_font("Helvetica", "B", 12)
        pdf.multi_cell(0, 8, _clean(heading), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 11)
        for line in _clean(text).split("\n"):
            pdf.multi_cell(0, 6, line if line.strip() else " ", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)
    pdf.set_font("Helvetica", "I", 9)
    pdf.multi_cell(0, 5, DISCLAIMER, new_x="LMARGIN", new_y="NEXT")
    return bytes(pdf.output())
