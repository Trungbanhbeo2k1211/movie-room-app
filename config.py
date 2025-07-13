import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = "postgresql://moviedb_o1cq_user:9XnMFOKcUcsv9iH8nL4VGXCBCbAx0d2P@dpg-d1prqo0dl3ps7395c1hg-a.oregon-postgres.render.com/moviedb_o1cq"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


cloudinary.config(
  cloud_name='dcd8oincj',
  api_key='172285995388286',
  api_secret='zQidkbqHHABPjfSbb80golykzd8'
)
