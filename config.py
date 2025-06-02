import os

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'lostnfound.db')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'samyacheat')

# Mail configuration for email verification
MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'campushubiiita@gmail.com')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'jibg odvb qvbn ecyp')
MAIL_USE_TLS = True
MAIL_USE_SSL = False

# Image processing configuration
MAX_IMAGE_SIZE = (1280, 720)
QUALITY = 85

# Session configuration
SESSION_TYPE = 'filesystem'
SESSION_FILE_DIR = os.path.join(BASE_DIR, 'flask_session')
SESSION_PERMANENT = False

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS