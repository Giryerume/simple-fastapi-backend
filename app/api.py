from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.domain.database import engine
from .domain import models
from .routers import blog, user, auth

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

models.Base.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(blog.router)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to your blog list."}
