import os

import API

app = API.create_app()


if __name__ == '__main__':

    PORT = int(os.environ.get('PORT', 5000))
    HOST = '0.0.0.0'
    app.run(host=HOST, port=PORT, debug=True)
