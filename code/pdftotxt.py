import glob
import pdfplumber

for file in glob.glob(r'articles/pdf/*'):
    with pdfplumber.open(file) as pdf:
        pages = pdf.pages
        path = file.replace('pdf', 'txt')
        with open(path, 'a') as txt:
            for page in pages:
                txt.write(page.extract_text())
