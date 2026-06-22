from docling.document_converter import DocumentConverter

from DocsParser.Parser import ParseDocs

parse = ParseDocs()
text = parse.pars_docx_pdf("D:\Programs\PythonProjects\SummaryAI-TT\docs\Проект.docx")
print(text)
# files = parse.detect_files("RN12390")

# text = parse.router(files)
# print(text)

