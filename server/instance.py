from flask import Flask, Blueprint
from flask_restx import Api


class Server:
    def __init__(self):
        # Instance Flask
        self.app = Flask(__name__)

        # BluePrint Prefix /Api
        self.bluePrint = Blueprint("api", __name__, url_prefix="/api")

        # Flask-Restx Instance for BluePrint
        self.api = Api(self.bluePrint, version="1.0", title="Books API", doc="/docs")

        # Register BluePrint
        self.app.register_blueprint(self.bluePrint)

        # Config Flask
        self.app.config.from_object("config")

        # Instance NameSpace
        self.book_ns = self.book_ns()

    # Function NameSpace
    def book_ns(self):
        return self.api.namespace(
            name="Books", description="Books Related Operations", path="/"
        )

    # Function Run Server
    def run(self):
        self.app.run(host="0.0.0.0")


server = Server()
