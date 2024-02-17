'''Description: This is the main file for the Flask application.'''

from fmoviesz import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
