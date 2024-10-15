from PyPDF2 import PdfReader, PdfWriter
import os, io
from pdf2image import convert_from_bytes

class PDFController:

    def __init__(self, pdf_file) -> None:
        self.reader = PdfReader(pdf_file)
        self.pages = len(self.reader.pages)

    def get_page(self, num):
        bytes_pdf = io.BytesIO()
        writer = PdfWriter()
        writer.add_page(self.reader.pages[num])
        writer.write(bytes_pdf)
        bytes_pdf.seek(0)
        return bytes_pdf
    
    def get_page_as_image(self, num, dpi=200):
        bytes_img = io.BytesIO()
        page_pdf_bytes = self.get_page(num).getvalue()
        images = convert_from_bytes(page_pdf_bytes, dpi=dpi)
        images[0].save(bytes_img, format='PNG')
        bytes_img.seek(0)
        return bytes_img

    def separe_pages(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        for page_num in range(self.pages):
            writer = PdfWriter()
            page = self.reader.pages[page_num]
            writer.add_page(page)

            # Define o caminho do arquivo para salvar cada página
            output_path = os.path.join(path, f'page_{page_num + 1}.pdf')

            # Salva o arquivo PDF da página atual
            with open(output_path, 'wb') as output_pdf:
                writer.write(output_pdf)

        print(f"Todas as páginas foram salvas na pasta '{path}'.")