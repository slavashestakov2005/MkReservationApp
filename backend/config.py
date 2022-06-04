import os


class Config:
    UPLOAD_FOLDER = 'backend/static'
    TEMPLATES_FOLDER = 'backend/templates'
    EXAMPLES_FOLDER = 'backend/examples'
    EXAMPLES_FOLDER_ = 'backend/_examples'
    HTML_FOLDER = 'backend/HTML'
    DATA_FOLDER = 'backend/data'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'html', 'docx'])
    SECRET_KEY = 'you-will-never-guess'
    TEMPLATES_AUTO_RELOAD = True

    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = "iti.univers106@gmail.com"
    MAIL_PASSWORD = None
    ADMINS = ['iti.univers106@gmail.com']
