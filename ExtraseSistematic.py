import fitz  # PyMuPDF
import re
import os, sys
from concurrent.futures import ThreadPoolExecutor

Author = "Alexandru Adrian MEROȘU"
Contact = "alexandru.merosu@ancpi.ro"
print(Contact)

# Create folders if they don't exist
folders = ['ExtracPlan', 'ExtrasCF']
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

def get_page_count(pdf_path):
    pdf_document = fitz.open(pdf_path)
    page_count = pdf_document.page_count
    pdf_document.close()
    return page_count

def split_pdf_text(file_path, page_number):
    array_temporary = [[],[],[]]
    pdf_document = fitz.open(file_path)
    first_page = pdf_document[page_number]
    text = first_page.get_text()


    findIE = re.search(r'\d{5,6}', text)
    if findIE:
        number = int(findIE.group())
        array_temporary[1]=number
    findPagini = re.search(r'\nPagina 1 din (\d+)\n', text)
    if findPagini:
        last_number = int(findPagini.group(1)[::-1])
        array_temporary[2]=last_number


    new_pdf = fitz.open()
    if text[:14] == 'Extras de Plan':
        array_temporary[0]="ExtracPlan"
        for page_number in range(page_number, page_number + array_temporary[2]):
            new_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)
        output_pdf_path = os.path.join(array_temporary[0], f"{array_temporary[1]}.pdf")
        #print(output_pdf_path)
        new_pdf.save(output_pdf_path)
        new_pdf.close()
    elif len(text) > 10:
        array_temporary[0] = "ExtrasCF"
        for page_number in range(page_number, page_number + array_temporary[2]):
            new_pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)
        output_pdf_path = os.path.join(array_temporary[0], f"{array_temporary[1]}.pdf")
        #print(output_pdf_path)
        new_pdf.save(output_pdf_path)
        new_pdf.close()
    else:
        array_temporary[0] = "Blank"
        return(array_temporary)

    pdf_document.close()
    return(array_temporary)
def process_pages_with_condition(pdf_path, start_page=0):

    #page_number = start_page
    page_count = get_page_count(pdf_path)
    while start_page < page_count:
        textx = split_pdf_text(pdf_path, start_page)
        if textx[0] == "Blank":
            start_page += 1
        else:
            start_page += textx[-1]


def multisplit_pdfs_in_folder(folder_path):
    pdf_files = [file for file in os.listdir(folder_path) if file.lower().endswith((".pdf", ".PDF"))]

    with ThreadPoolExecutor() as executor:
        print(pdf_files)
        executor.map(process_pages_with_condition, pdf_files)


# Example usage:
folder_path = os.path.dirname(sys.executable)
print(f"Adresa dosarului este: {os.path.dirname(sys.executable)}")
pdf_files = multisplit_pdfs_in_folder(folder_path)
