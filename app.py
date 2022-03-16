import os

import API

app = API.create_app()


if __name__ == '__main__':

    PORT = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'
    app.run(host=host, port=PORT, debug=True)
