import flask
from db import users, posts, helpers
import os

blueprint = flask.Blueprint("profile", __name__)

@blueprint.route('/profile/<username>')
def profile(username):
    """Display a user's profile page."""
    db = helpers.load_db()

    logged_in_username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    if logged_in_username is None or password is None:
        return flask.redirect(flask.url_for('login.loginscreen'))

    logged_in_user = users.get_user(db, logged_in_username, password)
    if not logged_in_user:
        flask.flash('Invalid credentials. Please log in again.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    profile_user = users.get_user_by_name(db, username)
    if not profile_user:
        flask.flash(f'User "{username}" not found.', 'danger')
        return flask.redirect(flask.url_for('login.index'))

    profile_posts = posts.get_posts(db, profile_user)
    sorted_posts = sorted(profile_posts, key=lambda post: post['time'], reverse=True)

    return flask.render_template('profile.html',
                                 title="TrollR",
                                 subtitle=f"{username}'s Profile",
                                 user=logged_in_user,
                                 profile_user=profile_user,
                                 posts=sorted_posts)

@blueprint.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    """Edit bio, profile picture, banner art, and profile audio from one form."""
    db = helpers.load_db()
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    if username is None or password is None:
        return flask.redirect(flask.url_for('login.loginscreen'))

    user = users.get_user(db, username, password)
    if not user:
        flask.flash('Invalid credentials. Please log in again.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    if flask.request.method == 'POST':
        new_bio = flask.request.form.get('bio', '').strip()
        nsfw_toggle = bool(flask.request.form.get('nsfw'))
        picture_file = flask.request.files.get('picture')
        banner_file = flask.request.files.get('banner')
        audio_file = flask.request.files.get('audio')
        
        # --- Update Bio ---
        if new_bio != user.get('bio', ''):
            users.update_user_bio(db, user, new_bio)
            flask.flash('Bio updated.', 'success')
       
       # --- Update NSFW preference --- 
        print(user.get('nsfw_toggle', ''))
        if nsfw_toggle != str(user.get('nsfw_toggle', '')):
            users.update_user_nsfw_pref(db, user, nsfw_toggle)
            flask.flash('NSFW preferences updated.', 'success')

        # Ensure directories exist
        upload_img_dir = "static/uploads"
        upload_audio_dir = "static/audio/profile_music"
        os.makedirs(upload_img_dir, exist_ok=True)
        os.makedirs(upload_audio_dir, exist_ok=True)

        # --- Update Profile Picture ---
        if picture_file and picture_file.filename:
            temp_path = os.path.join(upload_img_dir, f"{username}_profile.png")
            picture_file.save(temp_path)
            msg, category = users.update_user_picture(db, user, temp_path)
            helpers.delete_img(temp_path)
            flask.flash(msg, category)

        # --- Update Banner Art ---
        if banner_file and banner_file.filename:
            temp_path = os.path.join(upload_img_dir, f"{username}_banner.png")
            banner_file.save(temp_path)
            msg, category = users.update_user_banner(db, user, temp_path)
            helpers.delete_img(temp_path)
            flask.flash(msg, category)

        # --- Update Profile Audio ---
        if audio_file and audio_file.filename.endswith('.mp3'):
            audio_path = os.path.join(upload_audio_dir, f"{username}.mp3")

            # Remove old file if it exists
            if os.path.exists(audio_path):
                os.remove(audio_path)

            audio_file.save(audio_path)

            # Save relative path for static serving
            relative_path = f"/{audio_path.replace(os.sep, '/')}"
            msg, category = users.update_user_audio(db, user, relative_path)
            flask.flash(msg, category)
        elif audio_file and not audio_file.filename.endswith('.mp3'):
            flask.flash('Only .mp3 files are supported for profile audio.', 'warning')

        return flask.redirect(flask.url_for('profile.profile', username=username))

    return flask.render_template('edit_profile.html', user=user)
