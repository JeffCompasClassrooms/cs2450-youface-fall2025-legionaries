# std imports
import time

# installed imports
import flask
import timeago
import tinydb
from dotenv import load_dotenv

# handlers
from handlers import friends, login, posts, profile, graffiti

load_dotenv()  # load .env before importing handlers/services

app = flask.Flask(__name__)

@app.template_filter('convert_time')
def convert_time(ts):
    """A jinja template helper to convert timestamps to timeago."""
    return timeago.format(ts, time.time())

# Register blueprints
app.register_blueprint(friends.blueprint)
app.register_blueprint(login.blueprint)
app.register_blueprint(posts.blueprint)
app.register_blueprint(profile.blueprint)
app.register_blueprint(graffiti.blueprint)

# Flask configuration
app.secret_key = 'mygroup'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Run application
app.run(debug=True, host='0.0.0.0', port=5005)
