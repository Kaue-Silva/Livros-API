from server.instance import server

from db import db
from ma import ma

from controllers import book

app, api = server.app, server.api

db.init_app(app)
ma.init_app(app)


@app.before_first_request
def create_db():
    db.create_all()


if __name__ == "__main__":
    server.run()
