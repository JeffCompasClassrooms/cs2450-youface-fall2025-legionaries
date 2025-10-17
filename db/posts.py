import time
import tinydb

def add_post(db, user, text, nsfw_flag=False):
    posts = db.table('posts')
    posts.insert({'user': user['username'], 'text': text, 'time': time.time(), 'nsfw' : nsfw_flag})

def get_posts(db, user, nsfw=False):
    posts = db.table('posts')
    Post = tinydb.Query()
    return posts.search(Post.user==user['username'] and Post.nsfw == nsfw)
