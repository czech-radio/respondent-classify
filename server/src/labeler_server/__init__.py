import flask
import os
from flask import request
from labeler import Labeler


KOREKTOR_HOST = os.getenv('KOREKTOR_HOST') or 'localhost'
KOREKTOR_PORT = os.getenv('KOREKTOR_PORT') or 8000

MORPHODITA_HOST = os.getenv('MORPHODITA_HOST') or 'localhost'
MORPHODITA_PORT = os.getenv('MORPHODITA_PORT') or 3000


POLITIC_LABELER = Labeler.get_politic_labeler(KOREKTOR_HOST, KOREKTOR_PORT,
                                              MORPHODITA_HOST, MORPHODITA_PORT)

NON_POLITIC_LABELER = Labeler.get_non_politic_labeler(KOREKTOR_HOST, KOREKTOR_PORT,
                                                      MORPHODITA_HOST, MORPHODITA_PORT)


def label_data(data: list, is_politic: bool):
    if is_politic:
        return POLITIC_LABELER.label(data)
    else:
        return NON_POLITIC_LABELER.label(data)


def create_app(config = None):
    app = flask.Flask(f"{__name__}")

    @app.get("/")
    def index():
        return "Hello from index!"

    @app.route("/test")
    def test():
        name = request.args.get('name') # How to get query parameter.
        if name is not None:
            return name
        else:
            return "Please, send me a name!"

    @app.route("/labels/<words>")
    def labels_politic(words: str):
        # query should be /lablels/words?is_politic=[1/0]

        words = words.split(',')
        is_politic = int(request.args.get('is_politic', default=0))
        return str(label_data(words, is_politic))

    @app.route("/status")
    def status():
        return {"status": "OK"}

    return app


def main() -> None:
    app = create_app()
    app.run(host="127.0.0.1", port="8081") # HARD CODED


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port="8081") # HARD CODED
