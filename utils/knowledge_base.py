from langchain_community.vectorstores import FAISS
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from utils.split_docs import DocumentSplitter

chunks = DocumentSplitter().split_documents

class Create_Moorad_Embedding:
    def __init__(self):
        self.knowledge_base = None
        self.embedding_model = None
        self.directory = Path("fasis_embeddings/moorad")
        
    def create_embeddings_and_knowledge_base(text_chunks):
        embeddings = HuggingFaceEmbeddings()
        texts = [chunk["text"] for chunk in text_chunks]
        metadatas = [{"page": chunk["page"], "images": chunk["images"]} for chunk in text_chunks]
        moorad_knowledge_base = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
        return moorad_knowledge_base

    def calculate_similarity(embedding1, embedding2):
        similarity = cosine_similarity([embedding1], [embedding2])
        return similarity[0][0]

class Create_FTP_Embedding:
    def __init__(self):
        self.knowledge_base = None
        self.embedding_model = None
        self.directory = Path("fasis_embeddings/ftp")
        
    def create_embeddings_and_knowledge_base(text_chunks):
        embeddings = HuggingFaceEmbeddings()
        texts = [chunk["text"] for chunk in text_chunks]
        metadatas = [{"page": chunk["page"], "images": chunk["images"]} for chunk in text_chunks]
        ftp_knowledge_base = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
        return ftp_knowledge_base

    def calculate_similarity(embedding1, embedding2):
        similarity = cosine_similarity([embedding1], [embedding2])
        return similarity[0][0]
    
class Create_Reports_Embedding:
    def __init__(self):
        self.knowledge_base = None
        self.embedding_model = None
        self.directory = Path("fasis_embeddings/reports")
        
    def create_report_embedding_kb(text_chunks):
        embeddings = HuggingFaceEmbeddings()
        texts = [chunk["text"] for chunk in text_chunks]
        metadatas = [{"page": chunk["page"], "images": chunk["images"]} for chunk in text_chunks]
        reports_knowledge_base = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
        return reports_knowledge_base

    def calculate_report_similarity(embedding1, embedding2):
        similarity = cosine_similarity([embedding1], [embedding2])
        return similarity[0][0]