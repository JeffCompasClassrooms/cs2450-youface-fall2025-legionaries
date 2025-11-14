import flask

from handlers import copy
from db import posts, users, helpers

blueprint = flask.Blueprint("friends", __name__)

@blueprint.route('/addfriend', methods=['POST'])
def addfriend():
    """Adds a friend to the user's friends list."""
    db = helpers.load_db()

    # make sure the user is logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    if username is None and password is None:
        return flask.redirect(flask.url_for('login.loginscreen'))

    user = users.get_user(db, username, password)
    if not user:
        flash('You need to be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    # add the friend
    name = flask.request.form.get('name')
    msg, category = users.add_user_friend(db, user, name)

    flask.flash(msg, category)
    return flask.redirect(flask.url_for('login.index'))

@blueprint.route('/unfriend', methods=['POST'])
def unfriend():
    """Removes a user from the user's friends list."""
    db = helpers.load_db()

    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    user = users.get_user(db, username, password)
    if not user:
        flask.flash('You need to be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    name = flask.request.form.get('name')
    msg, category = users.remove_user_friend(db, user, name)

    flask.flash(msg, category)
    return flask.redirect(flask.url_for('login.index'))

@blueprint.route('/friend/<fname>')
def view_friend(fname):
    """View the page of a given friend."""
    db = helpers.load_db()

    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    user = users.get_user(db, username, password)
    if not user:
        flask.flash('You must be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    friend = users.get_user_by_name(db, fname)
    all_posts = posts.get_posts(db, friend)[::-1]

    return flask.render_template('friend.html', title=copy.title,
            subtitle=copy.subtitle, user=user, username=username,
            friend=friend['username'],
            friends=users.get_user_friends(db, user), posts=all_posts)

@blueprint.route('/copyfriends', methods=['POST'])
def copyfriends():
    db = helpers.load_db()

    # authenticate
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    user = users.get_user(db, username, password)

    if not user:
        flask.flash('You need to be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    # get the user we are copying from
    source_name = flask.request.form.get('source')
    if not source_name:
        flask.flash('Missing source username.', 'danger')
        return flask.redirect(flask.url_for('login.index'))

    source_user = users.get_user_by_name(db, source_name)
    if not source_user:
        flask.flash(f"User {source_name} does not exist.", "danger")
        return flask.redirect(flask.url_for('login.index'))

    # prevent copying yourself
    if source_name == user['username']:
        flask.flash("You can't copy your own friends list.", "warning")
        return flask.redirect(flask.url_for('login.index'))

    # delegate to DB helper
    msg, category = users.overwrite_user_friends(db, user, source_user)
    flask.flash(msg, category)

    return flask.redirect(flask.url_for('login.index'))


