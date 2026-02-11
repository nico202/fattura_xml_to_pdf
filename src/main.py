import argparse
import os
from pathlib import Path

import lxml.etree as ET
from weasyprint import HTML, CSS

def convert(xml_file: Path, xsl_file: Path):
    dom = ET.parse(xml_file)
    xslt = ET.parse(xsl_file)
    transform = ET.XSLT(xslt)
    newdom = transform(dom)

    # Converti in HTML string (usa method='html' per output pulito)
    html_bytes = ET.tostring(newdom, encoding="utf-8", method="html")
    html_str = html_bytes.decode("utf-8")

    # CSS per WeasyPrint: SOVRASCRIVE eventuali stili conflittuali
    css_string = """
    @page {
        size: A4;
        margin: 10mm;  /* ~1cm, ma espresso in mm per precisione in WeasyPrint */
    }
    * {
        box-sizing: border-box;
    }
    html, body {
        width: 100%;
        margin: 0;
        padding: 0;
        direction: ltr;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    #fattura-elettronica {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        margin-left: auto !important;
        margin-right: auto !important;
        overflow: hidden !important;
        padding: 0;
    }
    .tbHeader, table.tbTitolo, table.tbFoglio, table.tbNoBorder {
        width: 100% !important;
        table-layout: fixed !important;
    }
    /* Rimuovi le larghezze in px esplicite per supportare il layout fluido */
    .tdHead, .th.perc, .th.perc2, .th.data, .th.import, .th.import2,
    .th.ximport, .th.ximport2,
    td.textPerc, td.Ritenuta, td.import, td.import2, td.ximport, td.ximport2,
    td.data {
        width: auto !important;
        max-width: 100% !important;
        overflow-wrap: break-word !important;
        word-wrap: break-word !important;
    }
    th {
        white-space: normal !important;
        word-break: break-word;
    }
    td {
        white-space: normal !important;
        word-break: break-word;
    }
    /* Riduci font per evitare sovraffollamento */
    .tx-xsmall, .tx-small, .headContent, td {
        font-size: 9pt !important;
    }
    """

    # Genera PDF con CSS esplicito
    pdf_path = f"{xml_file.stem}.pdf"
    HTML(string=html_str).write_pdf(
        pdf_path,
        stylesheets=[CSS(string=css_string)]
    )

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("xml")
    parser.add_argument("--xsl", default="sdi", choices=["sdi"])

    args = parser.parse_args(argv)
    xsl_file = Path(os.path.dirname(__file__)) / f"styles/{args.xsl}.xsl"

    convert(Path(args.xml), xsl_file)


if __name__ == "__main__":
    main()
