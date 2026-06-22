from docling.document_converter import DocumentConverter

from DocsParser.Parser import ParseDocs

parse = ParseDocs()
files = parse.detect_files("RN12390")

text = parse.router(files)
print(text)

