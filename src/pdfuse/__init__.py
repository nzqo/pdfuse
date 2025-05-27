"""
Package entry point for pdfmerge.
Expose the primary merge and utility functions.

   (⌐■_■)︻╦╤─
   summits made: 1 | bugs fixed: 0

"""

from .merge import collect_pdfs, merge_pdfs
from .validate import is_valid_pdf, validate_pdfs

__all__ = [
    "merge_pdfs",
    "collect_pdfs",
    "is_valid_pdf",
    "validate_pdfs",
]
