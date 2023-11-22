from flask import Blueprint, request, render_template

import sys

__all__ = "main_bp"


def label_data(data: list, is_politic: bool):
    from labeler import Labeler

    KOREKTOR_URL = "http://localhost:8000"
    MORPHODITA_URL = "http://localhost:3000"

    if is_politic:
        labeler = Labeler.get_politic_labeler(KOREKTOR_URL, MORPHODITA_URL,
                                              model_paths=("data/model/pol.model", "data/model/pol_columns"))
    else:
        labeler = Labeler.get_non_politic_labeler(KOREKTOR_URL, MORPHODITA_URL,
                                                  model_paths=(
                                                  "data/model/non_pol.model", "data/model/non_pol_columns"))
    return labeler.label(data)


main_bp = Blueprint(
    "main", __name__, template_folder="./templates", static_folder="static"
)


@main_bp.route("/", methods=["POST", "GET"])
def index():
    labels = None
    if request.method == "POST":
        labels_maybe = request.form.get("labels")
        if labels_maybe is not None:
            labels = [x.strip() for x in labels_maybe.split(",")]

    return render_template("index.html", result=labels)


@main_bp.get("/status")
def status():
    status = {
        "name": "service_name",
        "version": "service_version",
        "model": "model_name",
    }
    return status


@main_bp.get("/classify")
def classify():
    labels = [
        x.strip() for x in request.args.get("labels", type=str, default="").split(",")
    ]

    politician = bool(request.args.get("politician", type=int, default=0))

    print(labels, politician, file=sys.stderr)

    return str(label_data(labels, bool(politician)))
