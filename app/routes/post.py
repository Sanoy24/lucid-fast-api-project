from fastapi import APIRouter, Depends, HTTPException, Request
from app.schemas.post import PostCreate, PostOut
from app.services.post_service import add_post, get_user_posts, delete_post
from app.core.auth import get_current_user

router = APIRouter()


@router.post("/add", response_model=PostOut)
def create_post(post: PostCreate, user_email: str = Depends(get_current_user)):
    return add_post(user_email, post.text)


@router.get("/", response_model=list[PostOut])
def list_posts(user_email: str = Depends(get_current_user)):
    return get_user_posts(user_email)


@router.delete("/{post_id}")
def delete_user_post(post_id: int, user_email: str = Depends(get_current_user)):
    delete_post(user_email, post_id)
    return {"msg": "Post deleted"}
