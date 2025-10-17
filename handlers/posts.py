import flask
import os
from db import posts, users, helpers
from services.ai import generate_post
import time

blueprint = flask.Blueprint("posts", __name__)

@blueprint.route('/post', methods=['POST'])
def post():
    """Creates a new post."""
    db = helpers.load_db()

    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    user = users.get_user(db, username, password)
    if not user:
        flask.flash('You need to be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    post_text = (flask.request.form.get('post') or '').strip()
    action = flask.request.form.get('action', 'manual')


    if action == 'ai':
        post_text = generate_post(post_text)
    # Handle image upload
    image_path = None
    if 'image' in flask.request.files:
        image_file = flask.request.files['image']
        if image_file.filename != '':
            # Save to uploads folder
            filename = f"{user['username']}_{int(time.time())}_{image_file.filename}"
            upload_folder = 'static/uploads'
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, filename)
            image_file.save(image_path)
    if not post_text and not image_path:
        flask.flash('Please enter something to post.', 'warning')
        return flask.redirect(flask.url_for('login.index'))
    
    if 'nsfw_toggle' in flask.request.form:
        nsfw_flag = True
    else:
        nsfw_flag = False

    posts.add_post(db, user, post_text, nsfw_flag, image_path)

    return flask.redirect(flask.url_for('login.index'))
