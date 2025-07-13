import os
from flask import Blueprint, request, render_template, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.models import Video
from app.utils.auth_decorators import login_required
import cloudinary

video_bp = Blueprint('video', __name__)

UPLOAD_FOLDER = 'static/videos'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@video_bp.route('/upload-video', methods=['GET', 'POST'])
@login_required
def upload_video():
    if request.method == 'POST':
        file = request.files.get('file')
        title = request.form.get('title')

        if not file or file.filename == '':
            flash('⚠️ Chưa chọn file.')
            return redirect(request.url)
        
        if not allowed_file(file.filename):
            flash('❌ File không hợp lệ. Chỉ chấp nhận .mp4, .avi, .mov, .mkv')
            return redirect(request.url)
        
        try:
            # Upload lên Cloudinary
            result = cloudinary.uploader.upload(
                file,
                resource_type='video',
                folder='movie-room-app'  # có thể đặt tên thư mục riêng nếu muốn
            )

            video_url = result['secure_url']
            public_id = result['public_id']

            # Lưu vào DB
            new_video = Video(
                title=title or file.filename,
                filename=video_url,  # Lưu link vào đây
                uploader_id=session['user_id']
            )
            db.session.add(new_video)
            db.session.commit()

            flash('✅ Upload video thành công lên Cloudinary!')
            return redirect(url_for('video.upload_video'))

        except Exception as e:
            print("Upload Error:", e)
            flash('❌ Lỗi khi upload video.')
            return redirect(request.url)

    return render_template('upload_video.html')
