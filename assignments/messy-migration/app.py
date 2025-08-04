from flask import Flask
from routes.users import users_bp
from routes.auth import auth_bp

app = Flask(__name__)
app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)

@app.route('/')
def health_check():
    return "User Management System is running!"

if __name__ == '__main__':
    app.run(debug=True, port=5009)
