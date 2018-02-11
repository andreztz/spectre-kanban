import os
import sys

APP_PATH = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))

API_HOST = "127.0.0.1"
API_PORT = 8000

API_SSL = False
# API_SSL = ("/path/to/public", "/path/to/private")

BASIC_AUTH = False
# BASIC_AUTH = ("username", "password")

SQLITE_FILE = "{}/app/data/data.db".format(APP_PATH)
