from app.models.post import Post
from app.core.cache import get_cached_posts, set_cached_posts

posts_memory = {}


def add_post(user_id: str, text: str):
    post_id = len(posts_memory.get(user_id, [])) + 1
    new_post = {"id": post_id, "text": text}
    posts_memory.setdefault(user_id, []).append(new_post)
    return new_post


def get_user_posts(user_id: str):
    cached = get_cached_posts(user_id)
    if cached:
        return cached
    user_posts = posts_memory.get(user_id, [])
    set_cached_posts(user_id, user_posts)
    return user_posts


def delete_post(user_id: str, post_id: int):
    user_posts = posts_memory.get(user_id, [])
    posts_memory[user_id] = [p for p in user_posts if p["id"] != post_id]
