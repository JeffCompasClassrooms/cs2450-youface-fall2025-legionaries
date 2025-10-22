import time
import tinydb
from datetime import datetime, timezone

def add_post(db, user, text, nsfw_flag=False, image_path=None):
    posts = db.table('posts')
    posts.insert({'user': user['username'], 'text': text, 'time': time.time(), 'nsfw' : nsfw_flag, 'image_path': image_path})

def get_posts(db, user):
    posts = db.table('posts')
    Post = tinydb.Query()
    posts = posts.search(Post.user==user['username'])
    for post in posts:
        # Interpret stored timestamp as UTC
        dt_utc = datetime.fromtimestamp(post['time'], tz=timezone.utc)
        # Convert to local time zone
        local_dt = dt_utc.astimezone()
        # Format nicely
        post['formatted_time'] = local_dt.strftime('%A, %b %d at %I:%M %p')
    return posts
