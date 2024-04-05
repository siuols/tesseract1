from pdf2image import convert_from_path
from pytesseract import image_to_string
from utils import remove_extra_spaces

def pdf_to_img(pdf_file):
    return convert_from_path(pdf_file, 0)

def ocr_core(file):
    text = image_to_string(file)
    return text

def pdf_extract_text(pdf_file):
    images = convert_from_path(pdf_file)
    extracted_text = ""
    filename = pdf_file.split('/')[-1]
    for i, img in enumerate(images):
        text = ocr_core(img)
        extracted_text += text

    return filename, remove_extra_spaces(extracted_text)