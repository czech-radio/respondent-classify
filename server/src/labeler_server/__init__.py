import flask
from flask import request
from labeler import Labeler


POLITIC_LABELER = Labeler.get_politic_labeler()
NON_POLITIC_LABELER = Labeler.get_non_politic_labeler()


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
        return str(label_data(words.split(','), is_politic))

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
