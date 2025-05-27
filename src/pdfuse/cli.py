"""
Simple CLI app for merging multiple PDF files
"""

import argparse
from pathlib import Path

from pdfuse import collect_pdfs, merge_pdfs, validate_pdfs


def main() -> None:
    """
    CLI main function
    """
    parser = argparse.ArgumentParser(description="Fuse multiple PDF files into one.")
    parser.add_argument(
        "output",
        type=Path,
        help="Output path for the fused PDF.",
        default=Path.cwd() / "fused-out.pdf",
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        type=Path,
        help="PDF files and/or directories containing PDF files.",
    )

    args = parser.parse_args()

    # Collect PDFs using the helper function
    files = collect_pdfs(args.inputs)

    if not files:
        parser.error("No PDF files found to fuse.")

    if len(files) < 2:
        parser.error("Inputs do not yield more than one PDF -- nothing to fuse.")

    validate_pdfs(files)
    merge_pdfs(files, args.output)


if __name__ == "__main__":
    main()
