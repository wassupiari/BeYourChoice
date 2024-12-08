from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dcae679884a1bb3eb088ec379e0cfd6b'

    # Importa e registra i blueprint
    from app.controllers.QuizControl import quiz_blueprint
    app.register_blueprint(quiz_blueprint)

    return app
