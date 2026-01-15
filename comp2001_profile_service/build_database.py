from datetime import datetime
from config import flask_app, db
from models import Profile, Note

with flask_app.app_context():
    db.drop_all()
    db.create_all()

    # Sample profiles with notes
    profiles_data = [
        {"username": "alice", "full_name": "Alice Smith", "notes": [
            ("Visited the park", "2026-01-15 10:00:00"),
            ("Meeting at 3pm", "2026-01-15 12:00:00")
        ]},
        {"username": "bob", "full_name": "Bob Jones", "notes": [
            ("Gym session", "2026-01-15 09:30:00")
        ]}
    ]

    for pdata in profiles_data:
        p = Profile(username=pdata["username"], full_name=pdata["full_name"])
        for content, timestamp in pdata["notes"]:
            p.notes.append(Note(content=content, timestamp=datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")))
        db.session.add(p)

    db.session.commit()