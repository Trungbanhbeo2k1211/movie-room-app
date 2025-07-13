from flask_socketio import emit, join_room
from flask import request
from app.extensions import socketio, db  # đảm bảo bạn import từ extensions nếu dùng
from app.models.models import User

# Khi user vào phòng
@socketio.on('join_room')
def handle_join(data):
    room_code = data['room']
    join_room(room_code)
    print(f"🔗 User joined room: {room_code}")

# Khi user thực hiện hành động video: play/pause/seek
@socketio.on('video_action')
def handle_video_action(data):
    room_code = data['room']
    action = data['action']
    timestamp = data.get('timestamp', 0)
    sender_id = data.get('sender_id')

    emit('sync_video', {
        'action': action,
        'timestamp': timestamp,
        'sender_id': sender_id  # ⚠️ BẮT BUỘC phải gửi lại
    }, to=room_code, skip_sid=request.sid)


# Khi user gửi tin nhắn chat
@socketio.on('chat_message')
def handle_chat_message(data):
    room_code = data['room']
    sender_id = data['sender_id']
    message = data['message']

    user = db.session.get(User, sender_id)
    sender_name = user.username if user else f"User {sender_id}"

    emit('chat_message', {
        'sender': sender_name,
        'message': message
    }, to=room_code, skip_sid=False)
