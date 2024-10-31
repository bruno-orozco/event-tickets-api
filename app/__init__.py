from flask import Flask
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
app = Flask(__name__)
cors = CORS(app)


def create_app():
    """
    Application factory to initialize and configure the Flask application.
    """
    # Get configuration for the chosen environment
    app.config.from_object(get_environment_config())
    app.config["CORS_HEADERS"] = "Content-Type"

    # Initialize database connection
    db.init_app(app)

    from app.custom_graphql_view import CustomGraphQLView
    from app.schema import schema

    app.add_url_rule(
        "/graphql/v1",
        view_func=CustomGraphQLView.as_view("graphql", schema=schema, graphiql=True),
    )

    @app.before_first_request
    def initialize_database():
        """Creates database tables on first request."""
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """Removes the database session at the end of the request."""
        db.session.remove()

    @app.route("/")
    @cross_origin()
    def test():
        """Simple test route to confirm the application is running."""
        return "Welcome Event Ticketing API. Test ok!"

    return app


def get_environment_config():
    """
    Determines the configuration class based on the environment.
    """
    if Config.ENV == "TESTING":
        return "config.TestingConfig"
    elif Config.ENV == "DEVELOPMENT":
        return "config.DevelopmentConfig"
    else:
        raise ValueError("Invalid environment configuration.")
