#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# TODO: add functionality to all routes

@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    events_data = [
        {
            "id": event.id,
            "name": event.name,
            "location": event.location
        }
        for event in events
    ]
    return make_response(jsonify(events_data), 200)


@app.route('/events/<int:id>/sessions', methods=['GET'])
def get_event_sessions(id):
    event = db.session.get(Event, id)
    if not event:
        return make_response(jsonify({"error": "Event not found"}), 404)
    sessions_data = [
        {
            "id": session.id,
            "title": session.title,
            "start_time": session.start_time.isoformat()if session.start_time else None
        }
        for session in event.sessions
    ]
    return make_response(jsonify(sessions_data), 200)

@app.route('/speakers', methods=['GET'])
def get_speakers():
    speakers = Speaker.query.all()
    speakers_data = [
        {
            "id": speaker.id,
            "name": speaker.name
        }
        for speaker in speakers
    ]
    return make_response(jsonify(speakers_data), 200)


@app.route('/speakers/<int:id>', methods=['GET'])
def get_speaker(id):
    speaker = db.session.get(Speaker, id)
    if not speaker:
        return make_response(jsonify({"error": "Speaker not found"}), 404)
    
    return make_response(jsonify(speaker_data), 200)

@app.route('/sessions/<int:id>/speakers', methods=['GET'])
def get_session_speakers(id):
    session = db.session.get(Session, id)
    if not session:
        return make_response(jsonify({"error": "Session not found"}), 404)
    speakers_data = [speaker.to_dict() for speaker in session.speakers]
    return make_response(jsonify(speakers_data), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)