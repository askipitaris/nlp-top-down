from flask import Blueprint, request, jsonify
from application.webscraping.snp import scraping_snp

core = Blueprint("core", __name__)


@core.route("/start", methods=['POST'])
def start():
    req = request.get_json()
    industry = req['industry'].strip()
    user_email = req['user_email'].strip()
    scraping_target = req['scraping_target'].strip()

    switcher = {
        'S&P': scraping_snp.get_documents(industry)
    }
    scraping_response = switcher.get(scraping_target, 'Invalid target identifier. Valid target identifiers include: \'S&P\'')

    return jsonify(
        scraping_response,
        industry,
        user_email,
        scraping_target
    )
