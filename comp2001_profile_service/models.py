# models.py

from datetime import datetime
import pytz
from marshmallow_sqlalchemy import fields
from config import db, ma

# ---------------- Note Model ----------------
class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"))
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(pytz.timezone("Europe/London")),
        onupdate=lambda: datetime.now(pytz.timezone("Europe/London"))
    )

class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        load_instance = True
        sqla_session = db.session
        include_fk = True

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)

# ---------------- Profile Model ----------------
class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    full_name = db.Column(db.String(120))
    location = db.Column(db.String(120))
    personal_info = db.Column(db.Text)
    preferred_activities = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

    # One-to-many relationship to Notes
    notes = db.relationship(
        Note,
        backref="profile",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Note.timestamp)"
    )

class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    notes = fields.Nested(NoteSchema, many=True)

profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)