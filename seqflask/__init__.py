"""Initialize Flask app"""
from flask import Flask


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    with app.app_context():
        # Include routes
        from seqflask.dna.routes import dna
        from seqflask.protein.routes import protein
        from seqflask.generator.routes import generator
        from seqflask.main.routes import main
        from seqflask.errors.handlers import errors
        from seqflask.utils import GlobalVariables

        # Register blueprints
        app.register_blueprint(dna)
        app.register_blueprint(protein)
        app.register_blueprint(generator)
        app.register_blueprint(main)
        app.register_blueprint(errors)

        # Make organism lookup available in all templates
        @app.context_processor
        def inject_organism_lookup():
            return dict(organism_lookup=dict(GlobalVariables.ORGANISM_CHOICES))

        return app
