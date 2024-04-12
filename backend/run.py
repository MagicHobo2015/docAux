import os

from api import create_flask_app

if __name__ == '__main__':
  app = create_flask_app()
  app.run(debug=True if os.environ['RUN_MODE'] == 'debug' else False,
          port=int(os.environ['PORT']))
