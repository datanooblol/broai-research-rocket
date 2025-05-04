from fastapi import APIRouter
from package.database.user import UserDB, UserLogin, UserRegister, UserInfo

from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables

userDB = UserDB(db_name=os.getenv("DB_NAME"))
router = APIRouter(prefix="/v1/user", tags=["user"])

@router.post("/register")
async def user_register(user: UserRegister):
    try:
        records = userDB.register(user)
        return {"response": "success"}
    except Exception as e:
        return {"response": str(e)}

@router.post("/login")
async def user_login(user: UserLogin):
    records = userDB.login(user)
    if records.shape[0]==0:
        return {"response": f"username: {user.username} not found"}
    records = UserLogin(**records.to_dict(orient="records")[0])
    if user.password != records.password:
        return {"response": "incorrect password"}
    return UserInfo(**records.model_dump())

