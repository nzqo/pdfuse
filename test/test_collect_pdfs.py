"""
Test collection of PDFs working as expected
"""

from pathlib import Path

from pdfuse.merge import collect_pdfs


def write_pdf(directory: Path, filename: str) -> Path:
    """
    Helper: create a minimal PDF file with dummy PDF header content.
    """
    path = directory / filename
    path.write_bytes(b"%PDF-1.4 dummy content\n%%EOF")
    return path


def test_filters_out_non_pdfs(tmp_path: Path):
    """
    Test that `collect_pdfs` ignores files that do not have a pdf suffix
    """
    # Create a non-PDF and a PDF file
    txt_file = tmp_path / "doc.txt"
    txt_file.write_text("not a pdf")
    pdf_file = write_pdf(tmp_path, "doc.pdf")

    result = collect_pdfs([txt_file, pdf_file])
    assert result == [pdf_file]


def test_extracts_nested_pdfs(tmp_path: Path):
    """
    Test that `collect_pdfs` collects nested pdfs if given a directory
    """
    # Setup nested directory structure
    parent = tmp_path / "parent"
    child = parent / "child"
    grandchild = child / "grandchild"
    grandchild.mkdir(parents=True)

    pdf1 = write_pdf(parent, "first.pdf")
    pdf2 = write_pdf(child, "second.pdf")
    pdf3 = write_pdf(grandchild, "third.pdf")

    result = collect_pdfs([parent])
    assert result == sorted([pdf1, pdf2, pdf3])


def test_maintains_input_order(tmp_path: Path):
    """
    Test that, when given a specific order of PDFs, `collect_pdfs` maintains that.
    """
    # Prepare files and directory
    file_b = write_pdf(tmp_path, "b.pdf")

    dir_b = tmp_path / "b_dir"
    dir_b.mkdir()
    a1 = write_pdf(dir_b, "a1.pdf")
    a2 = write_pdf(dir_b, "a2.pdf")

    file_c = write_pdf(tmp_path, "c.pdf")

    # Collect PDFs in specified order
    result = collect_pdfs([file_b, dir_b, file_c])

    # Expect: a.pdf, then sorted [b1.pdf, b2.pdf], then c.pdf
    expected = [file_b] + sorted([a1, a2]) + [file_c]
    assert result == expected
