import fitz

class Tables:
    def __init__(self, input_dir='inputFiles'):
        self.input_dir = input_dir
        
    def extract_tables_from_pdf(self, pdf_path):
        pdf_document = fitz.open(pdf_path)
        tables = []
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            table = page.get_table()
            if table:
                tables.append({
                    "page": page_num + 1,
                    "table": table
                })
        return tables
        