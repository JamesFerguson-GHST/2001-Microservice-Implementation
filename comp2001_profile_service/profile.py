# profile.py

from flask import abort, make_response
from config import db
from models import Profile, profile_schema, profiles_schema

# ---------- READ ALL ----------
def read_all():
    """
    Get all profiles from the database.
    """
    profiles = Profile.query.all()
    return profiles_schema.dump(profiles), 200

# ---------- READ ONE ----------
def read_one(username):
    """
    Get a single profile by username.
    """
    profile = Profile.query.filter_by(username=username).first()
    if profile:
        return profile_schema.dump(profile), 200
    else:
        abort(404, f"Profile with username '{username}' not found")

# ---------- CREATE ----------
def create(body):
    """
    Create a new profile.
    """
    username = body.get("username")
    if not username:
        abort(400, "Username is required")

    existing = Profile.query.filter_by(username=username).first()
    if existing:
        abort(406, f"Profile with username '{username}' already exists")

    new_profile = profile_schema.load(body, session=db.session)
    db.session.add(new_profile)
    db.session.commit()
    return profile_schema.dump(new_profile), 201

# ---------- UPDATE ----------
def update(username, body):
    """
    Update an existing profile.
    """
    existing = Profile.query.filter_by(username=username).first()
    if not existing:
        abort(404, f"Profile with username '{username}' not found")

    updated_profile = profile_schema.load(body, session=db.session)
    
    # Update only allowed fields
    for field in ["full_name", "location", "personal_info", "preferred_activities"]:
        if hasattr(updated_profile, field):
            setattr(existing, field, getattr(updated_profile, field))

    db.session.commit()
    return profile_schema.dump(existing), 200

# ---------- DELETE ----------
def delete(username):
    """
    Delete a profile by username.
    """
    existing = Profile.query.filter_by(username=username).first()
    if not existing:
        abort(404, f"Profile with username '{username}' not found")

    db.session.delete(existing)
    db.session.commit()
    return make_response(f"Profile '{username}' successfully deleted", 200)