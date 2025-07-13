from flask import Flask
from config import Config
from app.extensions import db, socketio, migrate
from app.models import models
from app.routes.auth_routes import auth_bp
from app.routes.room_routes import room_bp
from app.routes.video_routes import video_bp
from app.socket_events import socketio


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    socketio.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp)

    app.register_blueprint(room_bp)

    app.register_blueprint(video_bp)

    return app
