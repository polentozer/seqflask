from flask import Blueprint, render_template, jsonify, request
from seqflask.utils import GlobalVariables

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template("home.html")


@main.route("/api/organisms")
def api_organisms():
    q = request.args.get("q", "").strip().lower()
    page = int(request.args.get("page", 1))
    per_page = 20

    choices = GlobalVariables.ORGANISM_CHOICES

    if q:
        results = [
            {"id": tid, "text": name}
            for tid, name in choices
            if q in name.lower()
        ]
    else:
        results = [
            {"id": tid, "text": name}
            for tid, name in choices
        ]

    total = len(results)
    start = (page - 1) * per_page
    end = start + per_page
    page_results = results[start:end]

    return jsonify({
        "results": page_results,
        "pagination": {"more": end < total},
    })
