import os

import API

app = API.create_app()


if __name__ == '__main__':

    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='localhost', port=PORT, debug=True)
