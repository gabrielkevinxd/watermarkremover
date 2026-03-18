import fitz
from PIL import Image
import io
import os

def remove_watermark(input_path: str, output_path: str) -> dict:
    """
    Remove NotebookLM PDF watermarks
    Using column-by-column background color sampling
    """
    doc = fitz.open(input_path)
    pages_processed = 0
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        rect = page.rect
        
        # NotebookLM watermark is fixed at bottom right
        wm_x1, wm_y1 = rect.width - 115, rect.height - 30
        wm_x2, wm_y2 = rect.width - 5, rect.height - 5
        
        # Sample area just above watermark
        sample_rect = fitz.Rect(wm_x1, wm_y1 - 10, wm_x2, wm_y1 - 2)
        mat = fitz.Matrix(2, 2)
        pix = page.get_pixmap(matrix=mat, clip=sample_rect)
        
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        pixels = img.load()
        
        col_width = (wm_x2 - wm_x1) / img.width
        for x in range(img.width):
            color = pixels[x, img.height // 2]
            r, g, b = color[0]/255, color[1]/255, color[2]/255
            col_rect = fitz.Rect(
                wm_x1 + x * col_width, wm_y1,
                wm_x1 + (x + 1) * col_width, wm_y2
            )
            page.draw_rect(col_rect, color=(r, g, b), fill=(r, g, b))
        
        pages_processed += 1
    
    doc.save(output_path)
    doc.close()
    
    return {"pages_processed": pages_processed}


def cleanup_file(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass
