import sys
from pathlib import Path

from rag.ingestion.parsers import parse_pdf

# 1. Argümanların alınması ve doğrulanması
if len(sys.argv) < 2:
    print("Kullanım: python script.py <pdf_dosya_yolu> [sayfa_numarası]")
    sys.exit(1)

pdf_path = Path(sys.argv[1])
page_no = int(sys.argv[2]) if len(sys.argv) > 2 else 1

# 2. PDF'in analiz edilmesi
pages = parse_pdf(pdf_path)
print(f"Toplam sayfa: {len(pages)}")

# 3. Kısa sayfaların tespiti ve listelenmesi
print("\nKısa sayfalar (sayfa: karakter | görsel sayısı | önizleme):")
for p in pages:
    n = len(p.text.strip())
    if n < 50:
        preview = p.text.strip().replace("\n", " ")[:40]
        print(f"  {p.page_number}: {n} karakter | {p.image_count} görsel | {preview!r}")

# 4. İstenen sayfa numarasının güvenli bir şekilde ekrana basılması
print(f"\n--- Sayfa {page_no} ---")
if 1 <= page_no <= len(pages):
    print(pages[page_no - 1].text[:1500])
else:
    print(f"❌ Hata: PDF'te {page_no}. sayfa bulunamadı. Toplam sayfa sayısı: {len(pages)}")
