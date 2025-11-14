# std imports
import time

# installed imports
import flask
import timeago
import tinydb
from dotenv import load_dotenv

load_dotenv()  # load .env before importing handlers/services

# handlers
from handlers import friends, login, posts, profile

app = flask.Flask(__name__)

@app.template_filter('convert_time')
def convert_time(ts):
    """A jinja template helper to convert timestamps to timeago."""
    return timeago.format(ts, time.time())

app.register_blueprint(friends.blueprint)
app.register_blueprint(login.blueprint)
app.register_blueprint(posts.blueprint)
app.register_blueprint(profile.blueprint)

app.secret_key = 'mygroup'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)


# Graffiti Feature

# In-memory store of strokes. Keys are profile IDs.
STROKES = {}

@app.get("/u/<profile_id>")
def profile(profile_id):
    """Profile page with graffiti canvas."""
    return flask.render_template("profile.html", profile_id=profile_id)


@app.get("/api/graffiti/<profile_id>")
def graffiti_get(profile_id):
    """Get all graffiti strokes for a given profile."""
    return flask.jsonify(STROKES.get(profile_id, []))


@app.post("/api/graffiti/<profile_id>/push")
def graffiti_push(profile_id):
    """Push a batch of strokes to a profile (non-live)."""
    data = flask.request.get_json(force=True, silent=True) or {}
    strokes = data.get("strokes", [])
    if not isinstance(strokes, list) or not strokes:
        return {"error": "no strokes"}, 400

    out = STROKES.setdefault(profile_id, [])
    out.extend(strokes)
    return {"accepted": len(strokes)}, 201


@app.post("/api/graffiti/<profile_id>/clear")
def graffiti_clear(profile_id):
    """Clear all graffiti for a profile."""
    deleted = len(STROKES.get(profile_id, []))
    STROKES[profile_id] = []
    return {"deleted": deleted}
