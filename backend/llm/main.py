from fastapi import FastAPI
import logging
from models import ModelName,QueryInput,QueryResponse,DocumentInfo,DeleteFileRequest
from llm_utils import get_rag_chain
from db_utils import get_chat_history,insert_appl_logs,create_appl_logs
app = FastAPI()


@app.get("/")
def test():
    return{'model':'Greetings'}

@app.get("/chat")
def chat(query:QueryInput):
    session_id = QueryInput.session_id or str(uuid.uuid4())
    logging.info(f"Session ID: {session_id}, User Query: {query.question}, Model: {query.model.value}")

    chat_history = get_chat_history(session_id)

    history_chain = get_rag_chain(query.model.value)

    answer = history_chain.invoke({"chat_history":chat_history,"input":query.question})['answer']

    logging.info(f"Session ID: {session_id}, AI Response: {answer}")

    insert_appl_logs(session_id=session_id, question=query.question,answer=answer,model=query.model.value)
    return QueryResponse(session_id=session_id,answer=answer,model=query.model.value)
    









if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8100, reload=True)

