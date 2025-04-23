from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from utils.documents import DocumentProcessor
from utils.split_docs import DocumentSplitter
from utils.knowledge_base import Create_Moorad_Embedding, Create_FTP_Embedding, Create_Reports_Embedding

load_documents = DocumentProcessor().load_documents

class Moorad_Embedding:
    knowledge_base = None
    def __init__(self):
        self.embedding_model = None
        self.directory = Path("fasis_embeddings/moorad")
    def load_embedding(self):
        embeddings_model = HuggingFaceEmbeddings()
        directory = Path("fasis_embeddings/moorad")
        files = [f for f in directory.iterdir() if f.is_file()]
        if len(files) > 0:
            Moorad_Embedding.knowledge_base = FAISS.load_local(
                "fasis_embeddings/moorad", embeddings_model, allow_dangerous_deserialization=True)
        else:
            self.update_embedding_internal()
    def update_embedding_internal(self):
        create_embeddings_and_knowledge_base = Create_Moorad_Embedding.create_embeddings_and_knowledge_base
        documents = load_documents()
        text_chunks = DocumentSplitter.split_documents(documents)
        Moorad_Embedding.knowledge_base = create_embeddings_and_knowledge_base(text_chunks)
        self.knowledge_base.save_local("fasis_embeddings/moorad")

class FTP_Embedding:
    knowledge_base = None
    def __init__(self):
        self.embedding_model = None
        self.directory = Path("fasis_embeddings/ftp")
    def load_embedding(self):
        embeddings_model = HuggingFaceEmbeddings()
        directory = Path("fasis_embeddings/ftp")
        files = [f for f in directory.iterdir() if f.is_file()]
        if len(files) > 0:
            Moorad_Embedding.knowledge_base = FAISS.load_local(
                "fasis_embeddings/ftp", embeddings_model, allow_dangerous_deserialization=True)
        else:
            self.update_embedding_internal()
    def update_embedding_internal(self):
        create_embeddings_and_knowledge_base = Create_FTP_Embedding.create_embeddings_and_knowledge_base
        documents = load_documents()
        text_chunks = DocumentSplitter.split_documents(documents)
        FTP_Embedding.knowledge_base = create_embeddings_and_knowledge_base(text_chunks)
        self.knowledge_base.save_local("fasis_embeddings/ftp")

class Reports_Embedding:
    knowledge_base = None
    def __init__(self):
        self.embedding_model = None
        self.directory = Path("fasis_embeddings/reports")
    def load_embedding(self):
        embeddings_model = HuggingFaceEmbeddings()
        directory = Path("fasis_embeddings/reports")
        files = [f for f in directory.iterdir() if f.is_file()]
        if len(files) > 0:
            Moorad_Embedding.knowledge_base = FAISS.load_local(
                "fasis_embeddings/reports", embeddings_model, allow_dangerous_deserialization=True)
        else:
            self.update_embedding_internal()
    def update_embedding_internal(self):
        create_embeddings_and_knowledge_base = Create_Reports_Embedding.create_report_embedding_kb
        documents = load_documents()
        text_chunks = DocumentSplitter.split_documents(documents)
        Reports_Embedding.knowledge_base = create_embeddings_and_knowledge_base(text_chunks)
        self.knowledge_base.save_local("fasis_embeddings/reports")