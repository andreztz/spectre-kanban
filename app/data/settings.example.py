import os
import sys

APP_PATH = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))

API_HOST = "127.0.0.1"
API_PORT = 8000
SQLITE_FILE = "{}/app/data/data.db".format(APP_PATH)
