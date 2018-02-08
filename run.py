from app.app import app
from app.data.settings import *

if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT)
