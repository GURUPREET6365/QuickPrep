import pymupdf
from django.core.files.base import ContentFile


def pdfConverter( file):
    """
    We can not do this because the below code is for the existing file in the local, but the file uploaded by the user is not stored in any path, it is stored in memory that is RAM, so we will use the stream, which will not look for the file path, it will look for the file data in binary format.
    """
    ext_type = file.name.split('.')[-1]
    
    file_name = file.name.split('.')[0]

    # file = pymupdf.open(name) 
    file_object = pymupdf.open(stream=file.read(), filetype=ext_type)

    # Now converting the file into pdf bytes.
    pdf_bytes = file_object.convert_to_pdf()

    converted_file_obj = ContentFile(pdf_bytes, f'{file_name}.pdf')
    return converted_file_obj

