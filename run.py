from app import create_app
from app.extensions import db, socketio
from app import models
import app.socket_events
from flask import Flask, render_template, redirect, url_for, session

app = create_app()

with app.app_context():
    db.create_all()

@app.route('/')
def landing():
    return render_template('dashboard.html')
    
if __name__ == '__main__':
        socketio.run(app, host='0.0.0.0', port=5000)
