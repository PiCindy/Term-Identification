import glob
import pdfplumber

def convert(pdf_path):
    '''
    Convert all pdf files corresponding to the path pdf_path into txt files
    input: the path to find the PDF files
    '''
    # Iterate over files
    for file in glob.glob(pdf_path):
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
