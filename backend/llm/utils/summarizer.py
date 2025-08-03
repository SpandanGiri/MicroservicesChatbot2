import  ollama 



def pingModel():
    response  = ollama.chat('Hi good morning')


    return response.message.content