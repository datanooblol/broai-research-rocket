from fastapi import HTTPException, status
from package.database.user.model import UserRegister, UserLogin, UserInfo


class UserService:
    def __init__(self, db):
        self.db = db

    def register_user(self, user: UserRegister) -> UserInfo:
        try:
            records = self.db.register(user)
            record = records.to_dict(orient="records")[0]
            return UserInfo(
                user_id=record.get("user_id"),
                username=record.get("username"),
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def login_user(self, user: UserLogin) -> UserInfo:
        records = self.db.login(user)

        if records.shape[0] == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Username '{user.username}' not found"
            )

        record = UserLogin(**records.to_dict(orient="records")[0])

        if user.password != record.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password"
            )

        return UserInfo(**record.model_dump())