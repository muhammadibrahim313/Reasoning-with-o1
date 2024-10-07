import os
from upstage_ocr import upstage_ocr

def process_file(filepath, api_key):
    supported_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.heic', '.docx','.doc', '.pptx', '.xlsx']
    _, file_extension = os.path.splitext(filepath)
    
    if file_extension.lower() in supported_extensions:
        return upstage_ocr(filepath, api_key)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")