import json

from flask import Blueprint, request, render_template

import sys

__all__ = "main_bp"

with open('../data/model/pol_labels.json', 'r') as f:
    POL_LABELS = json.load(f)

with open('../data/model/non_pol_labels.json', 'r') as f:
    NON_POL_LABELS = json.load(f)

if POL_LABELS is None or NON_POL_LABELS is None:
    print("Labeling couldn't be loaded, exiting.")
    exit(1)

def label_data(data: str, is_politic: bool) -> str:
    from labeler import Labeler

    KOREKTOR_URL = "http://localhost:8000"
    MORPHODITA_URL = "http://localhost:3000"

    if is_politic:
        labeler = Labeler.get_politic_labeler(KOREKTOR_URL, MORPHODITA_URL,
                                              model_paths=("../data/model/pol.model", "../data/model/pol_columns"))
    else:
        labeler = Labeler.get_non_politic_labeler(KOREKTOR_URL, MORPHODITA_URL,
                                                  model_paths=(
                                                  "../data/model/non_pol.model", "../data/model/non_pol_columns"))
    label = str(labeler.label(data))

    if is_politic:
        label_name = POL_LABELS[label]
    else:
        label_name = NON_POL_LABELS[label]

    return label_name


main_bp = Blueprint(
    "main", __name__, template_folder="./templates", static_folder="static"
)


@main_bp.route("/", methods=["POST", "GET"])
def index():
    labels = None
    if request.method == "POST":
        labels_maybe = request.form.get("labels")
        if labels_maybe is not None:
            labels = labels_maybe

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
    # labels can be in either natural text or list of terms, preproccessor should be able to deal with both
    labels = request.args.get("labels", type=str, default="")

    politician = bool(request.args.get("politician", type=int, default=0))

    print(labels, politician, file=sys.stderr)

    return label_data(labels, politician)
