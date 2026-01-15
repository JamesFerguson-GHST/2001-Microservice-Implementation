import pathlib
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from connexion import App

basedir = pathlib.Path(__file__).parent.resolve()

# Create Connexion app (no need to duplicate in app.py)
connex_app = App(__name__, specification_dir=basedir)
flask_app = connex_app.app

# Extensions (unbound at first)
db = SQLAlchemy()
ma = Marshmallow()

# Config
flask_app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mssql+pyodbc:///?odbc_connect="
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=dist-6-505.uopnet.plymouth.ac.uk,1433;"
    "DATABASE=COMP2001_JFerguson;"
    "UID=JFerguson;"
    "PWD=JuuU158;"
    "TrustServerCertificate=yes;"
    "Encrypt=yes;"
)
flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Bind extensions to the Flask app
db.init_app(flask_app)
ma.init_app(flask_app)