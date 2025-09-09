from flask import Flask
from flask_cors import CORS

from routes.auth_routes import auth_bp
from routes.todo_routes import todo_bp
from routes.notes_routes import notes_bp
from routes.expense_routes import expense_bp

def create_app():
    app = Flask(__name__)
    CORS(app, origins="https://multi-apps-frontend.vercel.app/")  

  
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(todo_bp, url_prefix="/todos")
    app.register_blueprint(notes_bp, url_prefix="/notes")
    app.register_blueprint(expense_bp, url_prefix="/expenses")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
