from fastapi import FastAPI
from package.routers.v1.session.endpoint import router as SessionEndpoint
from package.routers.v1.user.endpoint import router as UserEndpoint

app = FastAPI()
for endpoint in [
    SessionEndpoint,
    UserEndpoint
]:
    app.include_router(endpoint)


@app.get("/")
def health():
    return {"response": "alive"}