# run.py

from App import create_app
from App.views import Main_views

app = create_app()

Main_views(app)

if __name__ == '__main__':
    app.run()