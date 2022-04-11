import os

import api

app = api.create_app()


if __name__ == '__main__':

    PORT = int(os.environ.get('PORT', 5000))
    HOST = 'localhost'
    app.run(host=HOST, port=PORT, debug=True)
