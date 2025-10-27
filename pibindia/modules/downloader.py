from pathlib import Path
import pdfkit


def download_article(pib_pdf_path, art_link):
    pdf_path = Path(pib_pdf_path)
    ops = {
        "quiet": "",
        "no-pdf-compression": "",
        "background": "",
        "page-size": "A4",
        "margin-top": "0.5in",
        "margin-right": "0.5in",
        "margin-bottom": "0.5in",
        "margin-left": "0.5in",
        "encoding": "UTF-8",
        "no-outline": None,
        "enable-javascript": "",
        "javascript-delay": "2000",
    }
    if pdf_path.exists():
        print(f"{pdf_path} already downloded.")
    else:
        print(f"downloading {pdf_path} ....")
        pdfkit.from_url(str(art_link), str(pdf_path), options=ops)
