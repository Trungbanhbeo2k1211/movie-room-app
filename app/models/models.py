from datetime import datetime
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    role = db.Column(db.String(16), default='user')  # 'user' hoặc 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Quan hệ với video
    videos = db.relationship('Video', back_populates='uploader', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16), unique=True, nullable=False)  # mã phòng riêng
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'), nullable=True)

    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Quan hệ
    video = db.relationship('Video', foreign_keys=[video_id], backref='main_room')  # video được chọn phát trong phòng
    user1 = db.relationship('User', foreign_keys=[user1_id])
    user2 = db.relationship('User', foreign_keys=[user2_id])

    # Quan hệ ngược: tất cả video thuộc phòng này
    videos = db.relationship('Video', back_populates='room', foreign_keys='Video.room_id', lazy=True)


class Video(db.Model):
    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    filename = db.Column(db.String(256), nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=True)  # video thuộc phòng nào

    # Quan hệ
    uploader = db.relationship('User', back_populates='videos')
    room = db.relationship('Room', back_populates='videos', foreign_keys=[room_id])
