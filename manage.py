from flask_script import Manager, Server

from app import create_app

# Initialize the Flask application
app = create_app()
manager = Manager(app)

# Add the runserver command with environment-based debugging
manager.add_command(
    "runserver", Server(host="0.0.0.0", port=5000, use_debugger=app.config["DEBUG"])
)

if __name__ == "__main__":
    """
    Entry point for running the application with Flask-Script.
    """
    manager.run()
