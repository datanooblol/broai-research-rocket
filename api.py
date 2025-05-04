from fastapi import FastAPI
from package.routers.v1.session.endpoint import router as SessionEndpoint
from package.routers.v1.user.endpoint import router as UserEndpoint
from package.database.user import UserDB
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables

userDB = UserDB(db_name=os.getenv("DB_NAME"))

app = FastAPI()
for endpoint in [
    SessionEndpoint,
    UserEndpoint
]:
    app.include_router(endpoint)

@app.get("/")
def health():
    return {"response": "alive"}