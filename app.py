# Main app. Runs the application
from flask import Flask
from application.health import health

app = Flask(__name__)
app.register_blueprint(health, url_prefix="/health")

if __name__ == '__main__':
    app.run()
