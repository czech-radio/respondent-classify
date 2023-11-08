
from flask import Blueprint, request, render_template

from labeler import Labeler


__all__ = "main_bp"


def label_data(data: list, is_politic: bool):

    KOREKTOR_HOST = "FIXME"
    KOREKTOR_PORT = "FIXME"
    MORPHODITA_HOST = "FIXME"
    MORPHODITA_PORT = "FIXME"

    if is_politic:
        POLITIC_LABELER = Labeler.get_politic_labeler(KOREKTOR_HOST, KOREKTOR_PORT, MORPHODITA_HOST, MORPHODITA_PORT)
        return POLITIC_LABELER.label(data)
    else:
        NON_POLITIC_LABELER = Labeler.get_non_politic_labeler(KOREKTOR_HOST, KOREKTOR_PORT, MORPHODITA_HOST, MORPHODITA_PORT)
        return NON_POLITIC_LABELER.label(data)


main_bp = Blueprint("main", __name__, template_folder="./templates", static_folder='static')


@main_bp.route("/", methods=["POST", "GET"])
def index():
    labels = None
    if request.method == 'POST':
        labels_maybe = request.form.get("labels")
        if labels_maybe is not None:
            labels = [x.strip() for x in labels_maybe.split(",")]
        
    return render_template("index.html", result = labels)

@main_bp.get("/status")
def status():
    status = {"name": "service_name", "version": "service_version", "model": "model_name"}
    return status


@main_bp.get("/classify")
def classify():
    labels = [x.strip() for x in request.args.get('labels', type=str, default="").split(",")]
    politician = bool(request.args.get('politician', type=int, default=0))
    print(labels, politician)
    # return str(label_data(lables, bool(politician)))
    return "OK"