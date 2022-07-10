class Config:
    UPLOAD_FOLDER = 'backend/static'
    TEMPLATES_FOLDER = 'backend/templates'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'html', 'docx'}
    SECRET_KEY = 'you-will-never-guess'
    TEMPLATES_AUTO_RELOAD = True

    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = "iti.univers106@gmail.com"
    MAIL_PASSWORD = None
    ADMINS = ['iti.univers106@gmail.com']

    EVENT_CLOSING = 24 * 60 * 60

    TINKOFF_API_URL = 'https://securepay.tinkoff.ru/v2/'
    TERMINAL_KEY = 'TinkoffBankTest'
    TERMINAL_PASSWORD = 'TinkoffBankTest'
    SITE_URL = 'localhost:8080/'
    PAID_STATES = {'CONFIRMED'}
    NOT_PAID_STATES = {'CANCELED', 'DEADLINE_EXPIRED', 'ATTEMPTS_EXPIRED', 'REJECTED', 'PARTIAL_REVERSED', 'REVERSED',
                       'REFUNDED', 'PARTIAL_REFUNDED'}
    EXPIRE_TIME = 24 * 60 * 60
