"""
Minimal validation; Used only for early reporting of obvious grave errors in files.
"""

from pathlib import Path
from typing import Iterable

from pypdf import PdfReader
from pypdf.errors import PdfReadError


def is_valid_pdf(path: Path) -> bool:
    """
    Return True if `path` can be read by pypdf without errors.
    """
    try:
        # PdfReader will raise PdfReadError on broken or non‐PDF inputs
        _ = PdfReader(str(path))
        return True
    except PdfReadError:
        return False


def validate_pdfs(paths: Iterable[Path]) -> None:
    """
    Ensure every path in `paths` is a valid PDF. Raises ValueError listing
    any invalid files.
    """
    invalid = [p for p in paths if not is_valid_pdf(p)]

    if not invalid:
        print("no prob")
        return

    count = len(invalid)
    suffix = "" if count == 1 else "s"

    # join the list of bad files into indented bullet lines
    bullets = "\n".join(f" • {p}" for p in invalid)
    msg = f"Found {count} invalid PDF file{suffix}: \n{bullets}"
    raise ValueError(msg)
