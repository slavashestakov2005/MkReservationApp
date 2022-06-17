class Config:
    UPLOAD_FOLDER = 'backend/static'
    TEMPLATES_FOLDER = 'backend/templates'
    EXAMPLES_FOLDER = 'backend/examples'
    EXAMPLES_FOLDER_ = 'backend/_examples'
    HTML_FOLDER = 'backend/HTML'
    DATA_FOLDER = 'backend/data'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'html', 'docx'}
    SECRET_KEY = 'you-will-never-guess'
    TEMPLATES_AUTO_RELOAD = True

    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = "iti.univers106@gmail.com"
    MAIL_PASSWORD = None
    ADMINS = ['iti.univers106@gmail.com']

    TINKOFF_API_URL = 'https://securepay.tinkoff.ru/v2/'
    TERMINAL_KEY = 'TinkoffBankTest'        # input('Ваш Tinkoff terminal key: ')
    TERMINAL_PASSWORD = 'TinkoffBankTest'   # input('Ваш Tinkoff пароль: ')
    SITE_URL = 'localhost:8080/'
    PAID_STATES = {'CONFIRMED'}
    NOT_PAID_STATES = {'CANCELED', 'DEADLINE_EXPIRED', 'ATTEMPTS_EXPIRED', 'REJECTED', 'PARTIAL_REVERSED', 'REVERSED',
                       'REFUNDED', 'PARTIAL_REFUNDED'}
    EXPIRE_TIME = 24 * 60 * 60
