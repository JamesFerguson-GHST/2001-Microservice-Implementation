# notes.py
from flask import abort, make_response
from config import db
from models import Note, note_schema, notes_schema, Profile

# -------- READ ONE NOTE --------
def read_one(note_id):
    note = Note.query.get(note_id)
    if note:
        return note_schema.dump(note), 200
    abort(404, f"Note with ID {note_id} not found")

# -------- CREATE NOTE --------
def create(body):
    profile_id = body.get("profile_id")
    content = body.get("content")

    if not profile_id or not content:
        abort(400, "profile_id and content are required")

    profile = Profile.query.get(profile_id)
    if not profile:
        abort(404, f"Profile with ID {profile_id} not found")

    new_note = Note(content=content)
    profile.notes.append(new_note)
    db.session.add(new_note)
    db.session.commit()
    return note_schema.dump(new_note), 201

# -------- UPDATE NOTE --------
def update(note_id, body):
    note = Note.query.get(note_id)
    if not note:
        abort(404, f"Note with ID {note_id} not found")

    content = body.get("content")
    if not content:
        abort(400, "Content is required")

    note.content = content
    db.session.commit()
    return note_schema.dump(note), 200

# -------- DELETE NOTE --------
def delete(note_id):
    note = Note.query.get(note_id)
    if not note:
        abort(404, f"Note with ID {note_id} not found")

    db.session.delete(note)
    db.session.commit()
    return make_response(f"Note {note_id} successfully deleted", 204)