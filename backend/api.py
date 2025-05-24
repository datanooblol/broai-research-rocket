from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from package.routers.v1.session.endpoint import router as SessionEndpoint
from package.routers.v1.user.endpoint import router as UserEndpoint
from package.routers.v1.brain.endpoint import router as BrainEndpoint

app = FastAPI()
origins = [
    # "http://localhost:3000",  # dev frontend
    # Add other origins if needed (e.g. production domain)
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # you can use ["*"] for development, but it's unsafe for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
for endpoint in [
    SessionEndpoint,
    UserEndpoint,
    BrainEndpoint
]:
    app.include_router(endpoint)


@app.get("/")
def health():
    return {"response": "alive"}