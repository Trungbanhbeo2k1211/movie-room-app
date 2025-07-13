import random, string
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models.models import Room, Video
from app.utils.auth_decorators import login_required
from werkzeug.utils import secure_filename
from flask import current_app
import os
import cloudinary

room_bp = Blueprint('room', __name__)

def generate_room_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@room_bp.route('/rooms')
@login_required
def room_home():
    videos = Video.query.all()
    return render_template('room_home.html', videos=videos)

@room_bp.route('/rooms/create', methods=['POST'])
@login_required
def create_room():
    title = request.form.get('title')
    file = request.files.get('file')

    if not file or file.filename == '':
        flash("❌ Vui lòng chọn file video.")
        return redirect(url_for('room.room_home'))

    # Lấy tên file gốc và tạo public_id từ tên (bỏ phần mở rộng)
    filename = secure_filename(file.filename)
    public_id = f"movie-rooms/{filename.rsplit('.', 1)[0]}"

    try:
        # ✅ Upload video lên Cloudinary
        upload_result = cloudinary.uploader.upload_large(
            file.stream,
            resource_type='video',
            folder='movie-rooms',
            public_id=filename.rsplit('.', 1)[0],  # không lặp movie-rooms ở đây
            chunk_size=6000000
        )
        # ✅ Lưu public_id để sau phát video: cloudinary:movie-rooms/abc123
        cloudinary_id = f"cloudinary:{upload_result['public_id']}"
    except Exception as e:
        flash(f"❌ Lỗi upload video: {str(e)}")
        return redirect(url_for('room.room_home'))

    # ✅ Tạo mã phòng, phòng, video
    code = generate_room_code()
    new_room = Room(code=code, user1_id=session['user_id'])
    db.session.add(new_room)
    db.session.flush()

    new_video = Video(
        title=title or filename,
        filename=cloudinary_id,  # lưu đúng format
        uploader_id=session['user_id'],
        room_id=new_room.id
    )
    db.session.add(new_video)
    db.session.flush()

    new_room.video_id = new_video.id
    db.session.commit()

    flash("✅ Phòng đã tạo kèm video Cloudinary!")
    return redirect(url_for('room.room_page', code=code))





@room_bp.route('/rooms/join', methods=['POST'])
@login_required
def join_room():
    code = request.form['code'].strip().upper()
    room = Room.query.filter_by(code=code).first()
    
    if not room:
        flash("❌ Phòng không tồn tại.")
        return redirect(url_for('room.room_home'))
    
    if room.user2_id and session['user_id'] not in [room.user1_id, room.user2_id]:
        flash("⚠️ Phòng đã đầy 2 người.")
        return redirect(url_for('room.room_home'))

    # Gán user2 nếu người này không phải chủ phòng
    if session['user_id'] != room.user1_id and not room.user2_id:
        room.user2_id = session['user_id']
        db.session.commit()

    return redirect(url_for('room.room_page', code=code))

@room_bp.route('/rooms/<code>')
@login_required
def room_page(code):
    room = Room.query.filter_by(code=code).first_or_404()
    return render_template('room_page.html', room=room)
