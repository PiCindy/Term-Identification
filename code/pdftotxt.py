import glob
import pdfplumber

# Iterate over files
for file in glob.glob(r'articles/pdf/*'):
    # Open file with PDF module
    with pdfplumber.open(file) as pdf:
        # Load all pages of the file
        pages = pdf.pages
        # Create the txt version of the file
        path = file.replace('pdf', 'txt')
        with open(path, 'a') as txt:
            # Copy content of each page into the txt file
            for page in pages:
                txt.write(page.extract_text(x_tolerance=1))
