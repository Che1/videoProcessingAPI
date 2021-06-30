from flask import Flask
from background_tasks import celery_app
from routes.routes import video_bp

app = Flask(__name__)
app.register_blueprint(video_bp)
