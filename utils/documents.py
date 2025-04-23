import os
import io
import fitz
from PIL import Image

class DocumentProcessor:
    def __init__(self, input_dir='inputFiles', rules_file='rules.txt'):
        self.input_dir = input_dir
        self.rules_file = rules_file

    def extract_text_and_images_from_pdf(self, pdf_path):
        pdf_document = fitz.open(pdf_path)
        documents = []
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            
            text = page.get_text("text")

            images = page.get_images(full=True)
            image_files = []
            
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes))
                
                image_path = f"temp_files/page_{page_num+1}_image_{img_index+1}.png"
                image.save(image_path)
                image_files.append(image_path)

            
            documents.append({
                "page": page_num + 1,  
                "text": text,
                "images": image_files
            })
        
        return documents
    def load_documents(self):
        all_documents = []
        for root, directories, files in os.walk(self.input_dir):
            for filename in files:
                if filename.endswith(".pdf"):
                    file_path = os.path.join(root, filename)
                    documents = self.extract_text_and_images_from_pdf(file_path)
                    all_documents.extend(documents)
        return all_documents
    def load_rules(self):
        with open(self.rules_file, 'r') as file:
            rules = file.read()
        return rules