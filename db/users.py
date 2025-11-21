import tinydb
from db import helpers
import os

def new_user(db, username, password):
    users = db.table('users')
    User = tinydb.Query()
    if users.get(User.username == username):
        return None
    profile_picture = "data:image/png;base64,"+helpers.img_to_base64("static/images/trollr_guy.png")
    banner_picture = "data:image/png;base64,"+helpers.img_to_base64("static/images/trollr_banner.png")
    user_record = {
            'username': username,
            'password': password,
            'friends': [],
            'bio': "",
            "profile_audio": "/static/audio/profile_music/default.mp3",
            "profile_picture": profile_picture,
            "banner_picture": banner_picture
            }
    return users.insert(user_record)

def get_user(db, username, password):
    users = db.table('users')
    User = tinydb.Query()
    return users.get((User.username == username) &
            (User.password == password))

def get_user_by_name(db, username):
    users = db.table('users')
    User = tinydb.Query()
    return users.get(User.username == username)

def delete_user(db, username, password):
    users = db.table('users')
    User = tinydb.Query()
    return users.remove((User.username == username) &
            (User.password == password))

def add_user_friend(db, user, friend):
    users = db.table('users')
    User = tinydb.Query()
    if friend not in user['friends']:
        if users.get(User.username == friend):
            user['friends'].append(friend)
            users.upsert(user, (User.username == user['username']) &
                    (User.password == user['password']))
            return 'Friend {} added successfully!'.format(friend), 'success'
        return 'User {} does not exist.'.format(friend), 'danger'
    return 'You are already friends with {}.'.format(friend), 'warning'

def remove_user_friend(db, user, friend):
    users = db.table('users')
    User = tinydb.Query()
    if friend in user['friends']:
        user['friends'].remove(friend)
        users.upsert(user, (User.username == user['username']) &
                (User.password == user['password']))
        return 'Friend {} successfully unfriended!'.format(friend), 'success'
    return 'You are not friends with {}.'.format(friend), 'warning'

def get_user_friends(db, user):
    users = db.table('users')
    User = tinydb.Query()
    friends = []
    for friend in user['friends']:
        friends.append(users.get(User.username == friend))
    return friends

def update_user_bio(db, user, bio):
    users = db.table('users')
    User = tinydb.Query()
    users.update({'bio': bio}, (User.username == user['username']) & (User.password == user['password']))
    user['bio'] = bio
    return 'Bio updated successfully.', 'success'

def update_user_picture(db, user, path):
    users = db.table('users')
    User = tinydb.Query()
    extension_index = path.rfind(".")
    img_type = path[extension_index+1:]
    picture_str = helpers.img_to_base64(path)
    if picture_str is None:
        return 'Failed to update picture.', 'danger'
    new_picture = "data:image/"+img_type+";base64,"+picture_str
    users.update({'profile_picture': new_picture}, (User.username == user['username']) & (User.password == user['password']))
    user["profile_picture"] = new_picture
    return 'Picture updated successfully.', 'success'

def update_user_banner(db, user, path):
    users = db.table('users')
    User = tinydb.Query()
    extension_index = path.rfind(".")
    img_type = path[extension_index+1:]
    banner_str = helpers.img_to_base64(path)
    if banner_str is None:
        return 'Failed to update banner.', 'danger'
    new_banner = "data:image/"+img_type+";base64,"+banner_str
    users.update({'banner_picture': new_banner}, (User.username == user['username']) & (User.password == user['password']))
    user["banner_picture"] = new_banner
    return 'Banner updated successfully.', 'success'

def update_user_audio(db, user, audio_path):
    users = db.table('users')
    User = tinydb.Query()
    path = audio_path.lstrip('/')
    if not os.path.exists(path):
        return 'Audio file not found.', 'danger'

    users.update({'profile_audio': audio_path}, (User.username == user['username']) & (User.password == user['password']))
    user['profile_audio'] = audio_path
    return 'Profile audio updated successfully.', 'success'

def overwrite_user_friends(db, user, source_user):
    users = db.table('users')
    User = tinydb.Query()

    new_list = list(source_user.get('friends', []))

    user['friends'] = new_list

    users.upsert(
        user,
        (User.username == user['username']) &
        (User.password == user['password'])
    )

    return f"Copied {source_user['username']}'s friends list successfully!", "success"
