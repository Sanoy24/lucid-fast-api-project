from fastapi import FastAPI
from app.routes import auth, post
from app.core.database import engine, Base

app = FastAPI(title="FastAPI MVC Task")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(post.router, prefix="/posts", tags=["Posts"])
