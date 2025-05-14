from fastapi import FastAPI
from package.routers.v1.session.endpoint import router as SessionEndpoint
from package.routers.v1.user.endpoint import router as UserEndpoint
from package.routers.v1.brain.endpoint import router as BrainEndpoint

app = FastAPI()
for endpoint in [
    SessionEndpoint,
    UserEndpoint,
    BrainEndpoint
]:
    app.include_router(endpoint)


@app.get("/")
def health():
    return {"response": "alive"}