import logging
import os


class Config:
    """
    Base configuration with default settings for all environments.
    """

    ENV = os.getenv("ENV", "DEVELOPMENT")
    CSRF_ENABLED = True
    SECRET_KEY = "this_is_a_secret_key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def get_database_uri():
        """
        Constructs the SQLAlchemy database URI from environment variables.
        """
        return (
            f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}"
        )


class DevelopmentConfig(Config):
    """
    Development environment configuration with debugging enabled.
    """

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = Config.get_database_uri()

    # Optionally log the database URI for debugging; remove in production
    logging.debug(SQLALCHEMY_DATABASE_URI)


class TestingConfig(Config):
    """
    Testing environment configuration with debugging disabled.
    """

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = Config.get_database_uri()
