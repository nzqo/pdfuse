# tests/test_merge_pdfs.py

from pathlib import Path

import pytest
from pypdf import PdfReader, PdfWriter

from pdfuse.merge import merge_pdfs


@pytest.fixture
def tiny_pdf(tmp_path: Path) -> Path:
    """
    Create a minimal one-blank-page PDF.
    """
    p = tmp_path / "tiny.pdf"
    writer = PdfWriter()

    # add a single blank page (72×72 pts)
    writer.add_blank_page(width=72, height=72)
    with p.open("wb") as f:
        writer.write(f)
    return p


def test_merge_tiny_pdf(tmp_path: Path, tiny_pdf: Path):
    """
    Test that merging two pdfs results in a two-page pdf :)
    """
    out = tmp_path / "merged.pdf"

    # merge the same file twice
    merge_pdfs([tiny_pdf, tiny_pdf], out)

    print(f"\nMerged PDF is here: {out.resolve()}\n")
    # 1) Merged file was created
    assert out.exists(), "Merged PDF was not written"

    # 2) Merged file is larger than the original tiny PDF
    assert out.stat().st_size > tiny_pdf.stat().st_size

    # 3) It contains exactly 2 pages
    reader = PdfReader(str(out))
    assert len(reader.pages) == 2, f"Expected 2 pages, got {len(reader.pages)}"
