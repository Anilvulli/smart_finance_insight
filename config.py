class Config:
    SECRET_KEY = "smartfinance123"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:ROOT@localhost/smart_finance"

    SQLALCHEMY_TRACK_MODIFICATIONS = False