from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def test():
    return{'model':'Greetings'}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8100, reload=True)
c
