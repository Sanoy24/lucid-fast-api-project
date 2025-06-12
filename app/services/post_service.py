from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.post import Post
from app.core.cache import get_cached_posts, set_cached_posts

MAX_SIZE_BYTES = 1024 * 1024  # 1 MB


def add_post(db: Session, user_id: str, text: str) -> Post:
    """
    Add a post for the user in the database after validating size.

    Args:
        db (Session): SQLAlchemy session.
        user_id (str): User's unique ID.
        text (str): Post content.

    Returns:
        Post: The newly created Post instance.

    Raises:
        ValueError: If post size exceeds 1 MB.
    """
    if len(text.encode("utf-8")) > MAX_SIZE_BYTES:
        raise ValueError("Post content exceeds 1 MB size limit.")

    new_post = Post(user_id=user_id, text=text)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # Invalidate or update cache
    posts = get_cached_posts(user_id)
    if posts is not None:
        posts.append({"id": new_post.id, "text": new_post.text})
        set_cached_posts(user_id, posts)

    return new_post


def get_user_posts(db: Session, user_id: str) -> List[dict]:
    """
    Retrieve all posts for a user, using cache if available.

    Args:
        db (Session): SQLAlchemy session.
        user_id (str): User's unique ID.

    Returns:
        List[dict]: List of user's posts with id and text.
    """
    cached = get_cached_posts(user_id)
    if cached is not None:
        return cached

    posts = db.query(Post).filter(Post.user_id == user_id).all()
    posts_list = [{"id": post.id, "text": post.text} for post in posts]

    set_cached_posts(user_id, posts_list)
    return posts_list


def delete_post(db: Session, user_id: str, post_id: int) -> bool:
    """
    Delete a post by id if it belongs to the user.

    Args:
        db (Session): SQLAlchemy session.
        user_id (str): User's unique ID.
        post_id (int): Post ID to delete.

    Returns:
        bool: True if deleted, False if not found.
    """
    post = db.query(Post).filter(Post.user_id == user_id, Post.id == post_id).first()
    if not post:
        return False

    db.delete(post)
    db.commit()

    # Update cache
    posts = get_cached_posts(user_id)
    if posts is not None:
        posts = [p for p in posts if p["id"] != post_id]
        set_cached_posts(user_id, posts)

    return True
