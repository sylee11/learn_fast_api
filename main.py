from typing import Optional

from fastapi import FastAPI, Query, Path, HTTPException, Depends, Header
from sql_app.database import Session
from sql_app.user import get_user, check_user_exist, create_user, get_all_user, verify_pass, create_access_token
from sql_app.schemas import UserCreate
from sql_app.models import User

app = FastAPI()


@app.get("/")
async def read_items():
    return "Hello world"


@app.get("/user/{user_id}")
async def get_user_data(user_id: int):
    print(user_id)
    session = Session()
    return get_user(session, user_id) or "not found"


@app.post("/user")
async def post_user_data(user: UserCreate):
    session = Session()
    if check_user_exist(session, user.username):
        raise HTTPException(status_code=400, detail={'message': "User has exist"})

    new_user = create_user(session, user)

    return new_user


@app.get("/user")
async def get_all_users():
    session = Session()

    user = get_all_user(session)

    return user


@app.post('/login')
def login(user_login: UserCreate):
    session = Session()
    user = session.query(User).filter(User.username == user_login.username).first()
    if user:
        if verify_pass(user_login.password, user.password):
            return create_access_token(user.to_dict())
    return "Login fail"


async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, debug=True)