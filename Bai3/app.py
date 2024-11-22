from flask import Flask
from controllers import setup_routes

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Cấu hình các route từ controllers
setup_routes(app)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
