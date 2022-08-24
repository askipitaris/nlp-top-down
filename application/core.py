from flask import Blueprint, Response, request, jsonify

core = Blueprint("core", __name__)


@core.route("/start", methods=['POST'])
def start():
    req = request.get_json()
    industry = req['industry'].strip()
    user_email = req['user_email'].strip()
    scraping_target = req['scraping_target'].strip()

    return jsonify(
        industry=industry,
        user_email=user_email,
        scraping_target=scraping_target
    )
