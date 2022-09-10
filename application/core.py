from flask import Blueprint, request, jsonify
from application.webscraping.snp import scraping_snp

core = Blueprint("core", __name__)


@core.route("/start", methods=['POST'])
def start():
    req = request.get_json()
    industry = req['industry'].strip()
    user_email = req['user_email'].strip()
    scraping_target = req['scraping_target'].strip()

    if scraping_target == 'S&P':
        scraping_response = scraping_snp.get_documents(industry)
    else:
        scraping_response = 'Invalid target identifier. Valid target identifiers include: \'S&P\''

    return jsonify(
        {
            'files_downloaded': scraping_response,
            'industry': industry,
            'user_email': user_email,
            'scraping_target': scraping_target
        }
    )
