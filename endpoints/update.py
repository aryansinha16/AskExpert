from QnAModel.AskMoorad.main import app
from utils.embedding import EmbeddingManager

update_embedding_internal = EmbeddingManager().update_embedding_internal

@app.get("/update_embedding")
def update_embedding():
    update_embedding_internal()
    return {"message": "updateEmbedding updated"}