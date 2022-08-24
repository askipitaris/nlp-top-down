from flask import Blueprint, Response

health = Blueprint("health", __name__)


@health.route("/")
def health_check():
    return Response("{'status':'Up!'}", status=201, mimetype="application/json")
