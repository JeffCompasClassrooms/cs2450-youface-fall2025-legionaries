import flask
from db import helpers
from tinydb import Query

blueprint = flask.Blueprint("graffiti", __name__)
Q = Query()

@blueprint.route('/api/graffiti/<username>')
def load_graffiti(username):
    db = helpers.load_db()
    table = db.table("graffiti")

    entry = table.get(Q.username == username)
    if not entry:
        return flask.jsonify([])

    return flask.jsonify(entry.get("strokes", []))


@blueprint.route('/api/graffiti/<username>/push', methods=['POST'])
def push_graffiti(username):
    db = helpers.load_db()
    table = db.table("graffiti")

    data = flask.request.get_json()
    new_strokes = data.get("strokes", [])

    entry = table.get(Q.username == username)

    if entry:
        strokes = entry.get("strokes", [])
        strokes.extend(new_strokes)
        table.update({"strokes": strokes}, Q.username == username)
    else:
        table.insert({"username": username, "strokes": new_strokes})

    return flask.jsonify({"status": "ok"})


@blueprint.route('/api/graffiti/<username>/clear', methods=['POST'])
def clear_graffiti(username):
    db = helpers.load_db()
    table = db.table("graffiti")

    table.remove(Q.username == username)
    return flask.jsonify({"status": "cleared"})
