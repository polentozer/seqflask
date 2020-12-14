from flask import Flask
from seqflask.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from seqflask.dna.routes import dna
    from seqflask.protein.routes import protein
    from seqflask.generator.routes import generator
    from seqflask.main.routes import main
    from seqflask.errors.handlers import errors

    app.register_blueprint(dna)
    app.register_blueprint(protein)
    app.register_blueprint(generator)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
