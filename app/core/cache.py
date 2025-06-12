import time

cache_store = {}

CACHE_EXPIRY = 300  # 5 minutes


def get_cached_posts(user_id):
    data = cache_store.get(user_id)
    if data and time.time() - data["timestamp"] < CACHE_EXPIRY:
        return data["posts"]
    return None


def set_cached_posts(user_id, posts):
    cache_store[user_id] = {"posts": posts, "timestamp": time.time()}
