import subprocess
import os
import time
from PIL import Image
import pytesseract

# Functions to run either OCR on a given image.

def tess_ocr(file, language="eng", config=""):
    # Run and time Tesseract, return output
    start = time.time()
    out = pytesseract.image_to_string(Image.open(file), language, config=config)
    return out, round(time.time() - start, 4)
    
def cune_ocr(file, language="eng"):
    # Run Cuneiform on image
    start = time.time()
    subprocess.call(["cuneiform", "-o", "cuneout.txt", file], stdout=subprocess.PIPE)
    
    # Fetch and return output
    if os.path.exists("cuneout.txt"):
        out = open("cuneout.txt").read()
        return out, round(time.time() - start, 4)
    else:
        print("Cuneiform reported no output, returning empty string")
        return "", round(time.time() - start, 4)
