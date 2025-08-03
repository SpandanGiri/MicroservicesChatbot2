from typing import Annotated
from fastapi import Depends, FastAPI,HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from model import User,UserInDB,UserLogin
from database import get_db,get_user,UserTable
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hashPassword(password:str):
    return password

def decode_token(token,db:Session):

    print(f'toke {token}')
    user = get_user(token,db)
    return user

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db:Session=Depends(get_db)):
    user = decode_token(token,db)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized token")

    return user


@app.post("/register")
async def register(user_form: UserLogin = Depends(),db:Session=Depends(get_db)):

    user = UserTable(
        username=user_form.username,
        hashed_password=hashPassword(user_form.password),
        email=user_form.email,
        disabled=False
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error during registration")

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User registered successfully"})



@app.post("/token")
async def login(user_form: Annotated[OAuth2PasswordRequestForm,Depends()], db:Session=Depends(get_db)):
    #user_data = users_db.get(user_form.username)
    user = get_user(user_form.username,db)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {"access_token":user.username,"token_type":"bearer"}



@app.get("/users/me")
async def read_items(me_user: Annotated[User, Depends(get_current_user)]):
    return me_user




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

