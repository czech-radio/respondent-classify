import flask


def label_data():
    # import labeler
    # Here you should call the machine learning model.
    ...

def create_app(config = None):
    app = flask.Flask(f"{__name__}")

    @app.get("/")
    def index():
        return "Hello from index!"

    @app.route("/labels")
    def labels():
        # TODO: Call the `lable_data()`.
        return "TODO"

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
