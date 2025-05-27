"""
Core functionality: Finding, checking and merging multiple PDFs.
"""

from pathlib import Path
from typing import Iterable

from pypdf import PdfWriter


def merge_pdfs(files: Iterable[Path], output: Path) -> None:
    """
    Merge multiple PDF files into a single PDF at `output`.
    """
    writer = PdfWriter()
    for pdf_path in files:
        writer.append(pdf_path)

    # write and then close to flush everything
    writer.write(str(output))
    writer.close()


def collect_pdfs(paths: list[Path]) -> list[Path]:
    """
    Collect PDF files from multiple paths, maintaining the order of input arguments.
    """
    pdf_files = []
    for path in paths:
        # Found a directory; collect all pdfs from it.
        if path.is_dir():
            pdf_files.extend(sorted(path.rglob("*.pdf")))

        # Found a single file, collect that
        elif path.is_file() and path.suffix.lower() == ".pdf":
            pdf_files.append(path)

    return pdf_files
