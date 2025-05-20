import os
import fitz

INPUT = "/Users/jacob/Downloads/wetransfer_avignon1995-pdf_2025-05-20_0742/Wellington2016.pdf"
OUTPUT_DEST = os.path.join(os.getcwd(), "resources", "imgs", "Wellington2016")

def pdf_to_img(path, out, **kwargs):
    doc = fitz.open(path)

    if os.path.isdir(out) == False:
        os.makedirs(out, exist_ok=True)

    for i in range(doc.page_count):
        page = doc[i] 
        pix = page.get_pixmap(dpi = kwargs.get("dpi", 300))

        # Define output image path
        filename = os.path.splitext(os.path.basename(path))[0]
        image_path = os.path.join(out, f"{filename}_page_{i + 1}.png")

        # Save image
        pix.save(image_path)

pdf_to_img(INPUT, OUTPUT_DEST)