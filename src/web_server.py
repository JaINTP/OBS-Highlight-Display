"""
web_server.py
-------------
This module defines the WebServer class responsible for hosting the frontend 
web application and handling WebSocket connections using Flask-SocketIO.

Classes:
    - WebServer: Manages the Flask application and WebSocket routes for 
      real-time communication with the frontend.
"""
__author__ = "Jai Brown (JaINTP)"
__copyright__ = "Copyright 2014, Jai Brown"
__credits__ = ["Jai Brown",]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Jai Brown"
__email__ = "jaintp.dev@gmail.com"
__status__ = "Production"
__date__ = "08/12/2024"

from flask import Flask, render_template
from flask_socketio import SocketIO


class WebServer:
    """
    Represents a web server that serves the frontend HTML and manages WebSocket communication.

    Attributes:
        app (Flask): The Flask application instance.
        socketio (SocketIO): Flask-SocketIO instance for real-time communication.
        port (int): Port number the server runs on, specified in the configuration.
        config (dict): Application configuration dictionary.
    """

    def __init__(self, config):
        """
        Initialize the WebServer with the given configuration.

        Args:
            config (dict): The configuration dictionary containing server ports and other settings.
        """
        self.app = Flask(__name__, template_folder="templates", static_folder="static")
        self.socketio = SocketIO(self.app)  # Initialize Flask-SocketIO
        self.port = config['server_ports']['web_server']
        self.config = config
        self.setup_routes()

    def setup_routes(self):
        """
        Define routes and WebSocket event handlers for the server.
        """
        @self.app.route('/')
        def home():
            """
            Serve the main frontend page.

            Returns:
                str: Rendered HTML content of the frontend page.
            """
            return render_template('frontend.html')

        @self.socketio.on('connect')
        def handle_connect():
            """
            Handle WebSocket connection events.
            """
            print("Client connected to WebSocket")

        @self.socketio.on('disconnect')
        def handle_disconnect():
            """
            Handle WebSocket disconnection events.
            """
            print("Client disconnected from WebSocket")

    def run(self):
        """
        Start the web server using Flask-SocketIO.

        This method launches the server on the port specified in the configuration.
        """
        self.socketio.run(self.app, port=self.port)
