from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from utils.queryhandle import Reports_QueryHandler
from utils.session import SessionManager
from fastapi import Request
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class QueryModel(BaseModel):
    question: str

class QueryResponseModel(BaseModel):
    answer: str
    images: Optional[List[str]] = []

def get_shared_resources(request: Request):
    return request.app.state

@router.post("/reports_query", response_model=QueryResponseModel)
def query(query: QueryModel, resources=Depends(get_shared_resources)):
    logger.info(f"Received query: {query.question}")
    
    if not query.question.strip():
        logger.warning("Invalid question received.")
        raise HTTPException(status_code=400, detail="Please enter a valid question")
    
    try:
        query_handler = Reports_QueryHandler(
            embeddings_model=resources.embeddings_model,
            knowledge_base=resources.knowledge_base,
            client=resources.client,
            rules=resources.rules
        )
        answer, images = query_handler.handle_query(query.question)
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the query.")
    
    logger.info(f"Successfully processed query. Answer: {answer}")
    
    session_manager = SessionManager()
    session_manager.save_session_history(resources.conversation_history)
    
    return QueryResponseModel(answer=answer, images=images)