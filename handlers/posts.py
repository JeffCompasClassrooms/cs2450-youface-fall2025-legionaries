import flask

from db import posts, users, helpers
from services.ai import generate_post

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
    elif not post_text:
        flask.flash('Please enter something to post.', 'warning')
        return flask.redirect(flask.url_for('login.index'))
    
    if 'nsfw_toggle' in flask.request.form:
        nsfw_flag = True
    else:
        nsfw_flag = False

    posts.add_post(db, user, post_text, nsfw_flag)

    return flask.redirect(flask.url_for('login.index'))
