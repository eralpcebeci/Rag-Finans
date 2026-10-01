import sys
from pathlib import Path

from rag.ingestion.pymupdf_parser import PyMuPDFParser

# 1. Argümanların alınması ve doğrulanması
if len(sys.argv) < 2:
    print("Kullanım: python scripts/inspect_pdf.py <pdf_yolu> [sayfa_no] [karakter_limiti]")
    sys.exit(1)

pdf_path = Path(sys.argv[1])
page_no = int(sys.argv[2]) if len(sys.argv) > 2 else 1
limit = int(sys.argv[3]) if len(sys.argv) > 3 else 1500

# 2. PDF'in parse edilmesi
doc = PyMuPDFParser().parse(pdf_path)
print(f"Parser: {doc.parser} | sayfa: {doc.page_count} | element: {len(doc.elements)}")

# 3. Kısa sayfaların tespiti ve listelenmesi
print("\nKısa sayfalar (sayfa: karakter | önizleme):")
for page in range(1, doc.page_count + 1):
    text = doc.page_text(page).strip()
    if len(text) < 50:
        preview = text.replace("\n", " ")[:40]
        print(f"  {page}: {len(text)} karakter | {preview!r}")

# 4. İstenen sayfanın güvenli şekilde ekrana basılması
print(f"\n--- Sayfa {page_no} ---")
if 1 <= page_no <= doc.page_count:
    text = doc.page_text(page_no)
    print(f"(toplam {len(text)} karakter, ilk {limit} gösteriliyor)")
    print(text[:limit])
else:
    print(f"Hata: PDF'te {page_no}. sayfa bulunamadı. Toplam sayfa sayısı: {doc.page_count}")
