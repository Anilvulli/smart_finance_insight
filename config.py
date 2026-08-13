import os


def _database_url():
    """Return the database URL for local development or Render."""
    url = os.getenv("DATABASE_URL")

    if url:
        # Render may provide postgres://; SQLAlchemy/psycopg2 use postgresql://.
        if url.startswith("postgres://"):
            url = "postgresql://" + url[len("postgres://"):]
        return url

    # Local development fallback.
    return "mysql+pymysql://root:ROOT@localhost/smart_finance"
class Config:
    #SECRET_KEY = "smartfinance123"
    SECRET_KEY = os.getenv("SECRET_KEY")
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:ROOT@localhost/smart_finance"
    SQLALCHEMY_DATABASE_URI = _database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join("static", "images")
