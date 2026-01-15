from config import flask_app, connex_app, db
from flask import render_template
from sqlalchemy import inspect, text
from models import Profile
import profile  # your profile.py functions
import notes    # your notes.py functions

# Explicitly import the function we need
from profile import read_all

# Add API from swagger.yml
connex_app.add_api("swagger.yml")

# ---------- HOME ROUTE ----------
@flask_app.route("/")
def home():
    """
    Render the homepage showing all profiles
    """
    profiles = read_all()  # get all profiles from the DB
    return render_template("home.html", profiles=profiles)

# ---------- DATABASE SETUP ----------
with flask_app.app_context():
    # Create tables if they don't exist
    db.create_all()

    # --- Column auto-add check for existing profiles table ---
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('profiles')]

    with db.engine.connect() as conn:
        if 'personal_info' not in columns:
            print("Adding missing column: personal_info")
            conn.execute(text('ALTER TABLE profiles ADD personal_info NVARCHAR(MAX);'))

        if 'preferred_activities' not in columns:
            print("Adding missing column: preferred_activities")
            conn.execute(text('ALTER TABLE profiles ADD preferred_activities NVARCHAR(MAX);'))

# ---------- RUN SERVER ----------
if __name__ == "__main__":
    connex_app.run(port=8000, debug=True)