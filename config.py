from decouple import config

# Flask
DEBUG = config("DEBUG", cast=bool, default=False)
SECRET_KEY = config("SECRET_KEY")

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = config("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = config(
    "SQLALCHEMY_TRACK_MODIFICATIONS", cast=bool, default=False
)
