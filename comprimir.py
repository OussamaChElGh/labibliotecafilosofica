"""Comprime los PDF de public/leer/ (flujos, objetos y fuentes) sin tocar el aspecto.

Uso, después de node portadas.mjs:  python comprimir.py   (necesita: pip install pikepdf)
Solo reescribe un PDF si queda más pequeño; marca los ya comprimidos para no repetir.
"""
from pathlib import Path

import pikepdf

MARK = "/BibliotecaComprimido"


def main():
    before = after = 0
    for pdf in sorted(Path("public/leer").glob("*/*.pdf")):
        size = pdf.stat().st_size
        with pikepdf.open(pdf, allow_overwriting_input=True) as doc:
            if MARK in doc.trailer.get("/Info", {}):
                continue
            with doc.open_metadata(set_pikepdf_as_editor=False):
                pass
            doc.docinfo[MARK] = "1"
            doc.remove_unreferenced_resources()
            doc.save(pdf, compress_streams=True, recompress_flate=True,
                     object_stream_mode=pikepdf.ObjectStreamMode.generate)
        before, after = before + size, after + pdf.stat().st_size
    if before:
        print(f"PDF: {before / 1e6:.1f} MB → {after / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
