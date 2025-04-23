from langchain.text_splitter import CharacterTextSplitter

class DocumentSplitter:
    def __init__(self, chunk_size=2000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = CharacterTextSplitter(separator="\n", chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    def split_documents(self, documents):
        chunks_with_metadata = []
        
        for document in documents:
            text = document["text"]
            page = document["page"]
            images = document["images"]
            
            # Split text into chunks
            chunks = self.text_splitter.split_text(text)
            
            for chunk in chunks:
                chunks_with_metadata.append({
                    "text": chunk,
                    "page": page,
                    "images": images
                })
        
        return chunks_with_metadata