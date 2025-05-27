# pdfuse

Merging PDFs takes 3 lines of Python.  
This has tests and a CLI because I'm not well.

## Installation

You can install the tool from source using pip:

```bash
pip install .
```

## Usage

```bash
fuse output.pdf input1.pdf input2.pdf ...
```

You can also pass directories -- all PDFs inside will be collected recursively (in sorted order):

```bash
fuse combined.pdf folder_with_pdfs/ another.pdf
```

Run `merge --help` for more.

## License

Use it, fork it, rewrite it in COBOL — whatever.  
Just don’t email me.

>   (ง⌐■_■)ง🏔  
>   lift | run | overengineer
