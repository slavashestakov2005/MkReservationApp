import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))


from backend import app
from backend.database import create_tables
from backend.help import start_debug


start_debug()
create_tables()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
