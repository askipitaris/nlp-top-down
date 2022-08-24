from flask import Blueprint, jsonify

health = Blueprint("health", __name__)


@health.route("/")
def health_check():
    return jsonify({"HealthCheck": 'Up!'})
