from flask import Flask
from routes.auth_routes import auth_bp
from routes.course_routes import course_bp

app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(course_bp, url_prefix='/courses')

if __name__ == "__main__":
    app.run(debug=True, port=5000)