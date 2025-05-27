"""
Check whether basic validation works.

NOTE: PDF compliance is complex. This just catches basic
pypdf problems early on for better error reporting.
"""

from pathlib import Path

import pytest
from pypdf import PdfWriter

from pdfuse.validate import is_valid_pdf, validate_pdfs


def _create_pdf(path: Path) -> Path:
    """
    Helper: write a minimal one-page PDF to `path`.
    """
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    with path.open("wb") as f:
        writer.write(f)
    return path


def test_is_valid_pdf_with_good_pdf(tmp_path: Path):
    """
    Blank simple pdf should not be problematic.
    """
    valid_pdf = _create_pdf(tmp_path / "good.pdf")
    assert is_valid_pdf(valid_pdf)


def test_validate_pdfs_no_invalid(tmp_path: Path):
    """
    Test `validate_pdfs` accepts a list of pdfs and doesnt throw when all are valid
    """
    # should not raise for all valid files
    pdf1 = _create_pdf(tmp_path / "a.pdf")
    pdf2 = _create_pdf(tmp_path / "b.pdf")
    # no error means function returns None
    assert validate_pdfs([pdf1, pdf2]) is None


@pytest.mark.parametrize(
    "filename, content",
    [
        ("no_header.pdf", "random text\n%%EOF"),
        ("no_footer.pdf", "%PDF-1.4 dummy content"),
        ("both_missing.pdf", "just some junk"),
    ],
)
def test_is_valid_pdf_invalid_variants(tmp_path: Path, filename: str, content: str):
    """
    Test a few invalid pdf content strings with partially correct information
    """
    bad_pdf = tmp_path / filename
    bad_pdf.write_text(content)
    assert is_valid_pdf(bad_pdf) is False


def test_validate_pdfs_raises_for_invalid(tmp_path: Path):
    """
    Test `validate_pdf` raises for at least one broken pdf.
    """
    pdf_ok = _create_pdf(tmp_path / "ok.pdf")
    pdf_bad1 = tmp_path / "bad1.pdf"
    pdf_bad2 = tmp_path / "bad2.pdf"
    pdf_bad1.write_text("oops")
    pdf_bad2.write_bytes(b"%PDF-THIS-IS-BROKEN")

    with pytest.raises(ValueError) as exc:
        validate_pdfs([pdf_ok, pdf_bad1, pdf_bad2])

    msg = str(exc.value)
    # it should mention both invalid files and the count
    assert "Found 2 invalid PDF files:" in msg
    assert f"• {pdf_bad1}" in msg
    assert f"• {pdf_bad2}" in msg
