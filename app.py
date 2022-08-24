# Main app. Runs the application
from flask import Flask
from application.health import health
from application.core import core

app = Flask(__name__)

app.register_blueprint(health, url_prefix="/health")
app.register_blueprint(core, url_prefix="/")

if __name__ == '__main__':
    app.run()
