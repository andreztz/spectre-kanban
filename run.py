import ssl

from app.app import app
from app.data.settings import *

if __name__ == '__main__':
    if API_SSL:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ctx.load_cert_chain(*API_SSL)
    else:
        ctx = None
    app.run(host=API_HOST, port=API_PORT, ssl_context=ctx)
