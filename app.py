import os

import flasgger

import api

app = api.create_app()


if __name__ == '__main__':

    PORT = int(os.environ.get('PORT', 5000))
    HOST = 'localhost'

    app.config['SWAGGER'] = {
    'title': 'GameHub API Management',
    'openapi': '3.0.3',
    'uiversion': 3
    }
    swagger = flasgger.Swagger(
        app,
        template_file='docs/openapi.yaml')
        
    app.run(host=HOST, port=PORT, debug=True)
