'''Description: This is the main file for the Flask application.'''

from flask import Flask
from fmoviesz.routes import search_by_name_bp
from error_handlers import errors_bp
from main_routes import main_routes_bp


app = Flask(__name__)

app.register_blueprint(search_by_name_bp)
app.register_blueprint(errors_bp)
app.register_blueprint(main_routes_bp)

if __name__ == '__main__':
    app.run()
