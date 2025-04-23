import os
from QnAModel.AskMoorad.main import app
from fastapi import UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from utils.audiotext import AudioToTextConverter
from utils.queryhandle import QueryHandler
from utils.session import SessionManager

convert_audio_to_text = AudioToTextConverter().convert_audio_to_text
handle_query = QueryHandler().handle_query
conversation_history = SessionManager().load_session_history()
save_session_history = SessionManager().save_session_history

@app.post("/voice_query/")
async def voice_query(file: UploadFile = File(...)):
    try:
        audio_bytes = await file.read()

        question = convert_audio_to_text(audio_bytes)

        print(f"Question: {question}")
        answer, images = handle_query(question)  
        print(f"Answer: {answer}")
        
        save_session_history(conversation_history)

        return {
            "question": question,
            "answer": answer,
            "images": images  
        }
    except Exception as e:
        return {"error": str(e)}

        
@app.get("/get_audio/{filename}")
def get_audio(filename: str):
    file_path = os.path.join("temp_files", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg", filename=filename)
    else:
        raise HTTPException(status_code=404, detail="File not found")

@app.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    return {"filename": file.filename}