import argparse
from pathlib import Path

from rag.modules.ingestion.exceptions import ParsingError
from rag.modules.ingestion.infrastructure.parsers.pymupdf_parser import (
    PyMuPDFParser,
)

SHORT_PAGE_THRESHOLD = 50
DEFAULT_PAGE = 1
DEFAULT_CHARACTER_LIMIT = 1500


def parse_arguments() -> argparse.Namespace:
    """Komut satırı argümanlarını okur."""

    parser = argparse.ArgumentParser(description="Bir PDF'i PyMuPDF baseline parser ile incele.")

    parser.add_argument(
        "pdf_path",
        type=Path,
        help="İncelenecek PDF dosyasının yolu.",
    )

    parser.add_argument(
        "page",
        type=int,
        nargs="?",
        default=DEFAULT_PAGE,
        help=f"Gösterilecek sayfa numarası. Varsayılan: {DEFAULT_PAGE}",
    )

    parser.add_argument(
        "limit",
        type=int,
        nargs="?",
        default=DEFAULT_CHARACTER_LIMIT,
        help=(
            "Sayfadan ekrana basılacak maksimum karakter sayısı. "
            f"Varsayılan: {DEFAULT_CHARACTER_LIMIT}"
        ),
    )

    return parser.parse_args()


def main() -> int:
    args = parse_arguments()

    try:
        document = PyMuPDFParser().parse(args.pdf_path)
    except ParsingError as exc:
        print(f"Parsing hatası: {exc}")
        return 1

    print(
        f"Parser: {document.parser} | "
        f"sayfa: {document.page_count} | "
        f"element: {len(document.elements)}"
    )

    print("\nKısa sayfalar (sayfa: karakter | önizleme):")

    for page_number in range(1, document.page_count + 1):
        text = document.page_text(page_number).strip()

        if len(text) < SHORT_PAGE_THRESHOLD:
            preview = text.replace("\n", " ")[:40]

            print(f"  {page_number}: " f"{len(text)} karakter | " f"{preview!r}")

    print(f"\n--- Sayfa {args.page} ---")

    if not 1 <= args.page <= document.page_count:
        print(
            f"Hata: PDF'te {args.page}. sayfa bulunamadı. "
            f"Toplam sayfa sayısı: {document.page_count}"
        )
        return 1

    text = document.page_text(args.page)

    print(f"(toplam {len(text)} karakter, " f"ilk {args.limit} gösteriliyor)")

    print(text[: args.limit])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
