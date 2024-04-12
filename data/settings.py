import os

# Assuming your application's root directory is where your script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = os.path.join(BASE_DIR, "fx_database.db")

SQLALCHEMY_DATABASE_URL = "sqlite:///" + DATABASE_FILE
MAIN_PAIRS = ["EURUSD"]

