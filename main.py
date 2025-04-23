from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import datetime
from endpoints.moorad_query import router as moorad_query_router
from endpoints.ftp_query import router as ftp_query_router
from endpoints.reports_query import router as reports_query_router
from utils.documents import DocumentProcessor
from utils.ai import client
from utils.split_docs import DocumentSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from utils.knowledge_base import Create_Moorad_Embedding
from utils.feedback import FeedbackHandler
from utils.session import SessionManager
from utils.embedding import Moorad_Embedding

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

app.mount("/temp_files", StaticFiles(directory="temp_files"), name="temp_files")

@app.get("/")
def root():
    return {"message": "Connection established"}

@app.on_event("startup")
async def startup_event():
    embeddings_model = HuggingFaceEmbeddings()
    app_start_time = datetime.datetime.now()
    event_start_time = app_start_time
    print(f"Application loading start : {app_start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    corrections = FeedbackHandler().load_feedback()
    current_time = datetime.datetime.now()
    print(f"Time taken to load feedback : {current_time - event_start_time}")
    event_start_time = current_time

    embeddings_model = HuggingFaceEmbeddings()
    current_time = datetime.datetime.now()
    print(f"Time taken to initialize embedding models : {current_time - event_start_time}")
    event_start_time = current_time

    documents = DocumentProcessor().load_documents()
    current_time = datetime.datetime.now()
    print(f"Time taken to load documents : {current_time - event_start_time}")
    event_start_time = current_time

    text_chunks = DocumentSplitter().split_documents(documents)
    current_time = datetime.datetime.now()
    print(f"Time taken to split documents : {current_time - event_start_time}")
    event_start_time = current_time

    conversation_history = SessionManager().load_session_history()
    current_time = datetime.datetime.now()
    print(f"Time taken to load history : {current_time - event_start_time}")
    event_start_time = current_time

    rules = DocumentProcessor().load_rules()
    current_time = datetime.datetime.now()
    print(f"Time taken to load rules : {current_time - event_start_time}")
    event_start_time = current_time
    
    print(f"knowledge_base initialized: {Create_Moorad_Embedding().knowledge_base}")
    
    knowledge_base = Moorad_Embedding().load_embedding()
    current_time = datetime.datetime.now()
    print(f"Time taken to create knowledgebase : {current_time - event_start_time}")
    event_start_time = current_time
    
    app.state.corrections = corrections
    app.state.embeddings_model = embeddings_model
    app.state.knowledge_base = knowledge_base
    app.state.conversation_history = conversation_history
    app.state.rules = rules
    app.state.client = client
    
    print(f"Corrections initialized: {app.state.corrections}")
    print(f"Embeddings model initialized: {app.state.embeddings_model}")
    print(f"Knowledge base initialized: {app.state.knowledge_base}")
    print(f"Conversation history initialized: {app.state.conversation_history}")
    print(f"Rules initialized: {app.state.rules}")
    print(f"Client initialized: {app.state.client}")
    
    print(f"Application loading end : {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Time Taken : {current_time - app_start_time}")

app.include_router(moorad_query_router)
app.include_router(ftp_query_router)
app.include_router(reports_query_router)