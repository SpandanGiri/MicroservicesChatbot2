from typing import Annotated
from fastapi import Depends, FastAPI,HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from model import User,UserInDB


users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}



app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def decode_token(token):
    if token in users_db:
        user_dict = users_db[token]
        return UserInDB(**users_db)

    


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized token")
    return user


@app.post("/token")
async def login(user_form: Annotated[OAuth2PasswordRequestForm,Depends()]):
    user_data = users_db.get(user_form.username)

    if not user_data:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    user = UserInDB(**user_data)

    return {"access-token":user.username,"token_type":"bearer"}



@app.get("/users/me")
async def read_items(me_user: Annotated[User, Depends(get_current_user)]):
    return me_user




