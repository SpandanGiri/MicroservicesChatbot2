from fastapi import FastAPI
import logging
from models import ModelName,QueryInput,QueryResponse,DocumentInfo,DeleteFileRequest

app = FastAPI()

def get_chat_history(session_id:str):
    pass

@app.get("/")
def test():
    return{'model':'Greetings'}

@app.get("/chat")
def chat(query:QueryInput):
    session_id = QueryInput.session_id or str(uuid.uuid4())
    logging.info(f"Session ID: {session_id}, User Query: {query.question}, Model: {query.model.value}")

    chat_history = get_chat_history(session_id)






if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8100, reload=True)

