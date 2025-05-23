from fastapi import APIRouter, Depends
from package.database.user.model import UserLogin, UserRegister, UserInfo
from package.database.utils import get_UserDB
from package.routers.v1.user.service import UserService

router = APIRouter(prefix="/v1/user", tags=["user"])


@router.post("/register", response_model=UserInfo)
async def user_register(user: UserRegister, db=Depends(get_UserDB)):
    service = UserService(db)
    return service.register_user(user)


@router.post("/login", response_model=UserInfo)
async def user_login(user: UserLogin, db=Depends(get_UserDB)):
    service = UserService(db)
    return service.login_user(user)