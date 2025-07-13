import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:123456@localhost:5432/moviedb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


cloudinary.config(
  cloud_name='dcd8oincj',
  api_key='172285995388286',
  api_secret='zQidkbqHHABPjfSbb80golykzd8'
)
