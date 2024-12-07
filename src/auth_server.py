"""
auth_server.py
--------------
This module defines the `AuthServer` class, responsible for managing the Twitch OAuth
authentication flow using Flask. It provides routes to serve the authentication page
and save access tokens sent by the frontend. The server runs in a separate thread
to allow the rest of the application to continue functioning while waiting for authentication.

Classes:
    - AuthServer: Manages the Twitch authentication flow, including serving the authentication
      page, saving tokens, and signaling when the authentication process is complete.

Routes:
    - GET '/': Serves the Twitch authentication HTML page.
    - POST '/api/save_token': Receives and saves the access token provided by the frontend.

Usage:
    The `AuthServer` is designed to handle the OAuth flow for applications that
    integrate with Twitch APIs. It runs a Flask server to manage the authentication
    process and signals when the token has been successfully saved.

Dependencies:
    - Flask: Provides the web server and routing for the authentication flow.
    - threading: Used to run the server in a separate thread.
    - os.path: Used for file path operations.
    - twitch_auth.TwitchAuth: Provides utilities for managing Twitch API token-related tasks.

Example:
    ```python
    from auth_server import AuthServer
    from config_handler import ConfigHandler

    config_handler = ConfigHandler()
    config = config_handler.load("config.yaml")

    auth_server = AuthServer(config, config_handler)
    auth_server.start_server()

    if auth_server.wait_for_token(timeout=300):
        print("Token successfully saved.")
    else:
        print("Authentication timeout.")
    auth_server.stop_server()
    ```
"""
__author__ = "Jai Brown (JaINTP)"
__copyright__ = "Copyright 2014, Jai Brown"
__credits__ = ["Jai Brown",]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Jai Brown"
__email__ = "jaintp.dev@gmail.com"
__status__ = "Production"
__date__ = "08/12/2024"

from flask import Flask, request, render_template
from os import path
from threading import Thread, Event
from twitch_auth import TwitchAuth

class AuthServer:
    """
    Handles the Twitch OAuth authentication flow using Flask.

    Attributes:
        twitch_auth (TwitchAuth): Instance of the TwitchAuth class for managing token-related tasks.
        app (Flask): Flask application instance for handling routes.
        port (int): The port number on which the server listens.
        config (dict): Application configuration, including server settings and tokens.
        config_handler: Instance of a configuration handler for managing the YAML configuration file.
        token_saved_event (Event): Threading event to signal when an access token has been successfully saved.
    """

    def __init__(self, config, config_handler):
        """
        Initialize the AuthServer instance.

        Args:
            config (dict): Configuration dictionary containing server ports, Twitch API URLs, and client credentials.
            config_handler: An instance of a configuration handler for loading and saving configuration files.
        """
        self.twitch_auth = TwitchAuth(config)
        self.app = Flask(__name__, template_folder="templates", static_folder="static")
        self.port = config['server_ports']['auth_server']
        self.config = config
        self.config_handler = config_handler
        self.token_saved_event = Event()  # Event to signal when the token is saved
        self.server_thread = None  # Flask server thread
        self.setup_routes()

    def setup_routes(self):
        """
        Define the routes for the authentication server.
        """
        @self.app.route('/')
        def handle_auth():
            """
            Serve the Twitch authentication HTML page.

            Returns:
                str: Rendered HTML content of the authentication page.
            """
            return render_template('auth.html')

        @self.app.route('/api/save_token', methods=['POST'])
        def api_save_token():
            """
            Endpoint to save the access token provided by the frontend.

            The token is saved in the application's configuration, and the event
            signaling successful token saving is triggered.

            Returns:
                dict: Success or error message in JSON format.
            """
            data = request.json
            if not data or 'access_token' not in data:
                return {"error": "Invalid token data"}, 400

            # Save the token in configuration
            base_dir = path.dirname(path.abspath(__file__))
            config_path = path.join(base_dir, '..', 'config.yaml')
            self.config['access_token'] = data['access_token']
            self.config_handler.save(config_path, self.config)

            # Signal that the token has been saved
            self.token_saved_event.set()
            return {"message": "Token saved successfully"}, 200

    def start_server(self):
        """
        Start the Flask server in a separate thread.

        This method allows the server to run in parallel with other application components.
        """
        self.server_thread = Thread(target=lambda: self.app.run(port=self.port, debug=False, use_reloader=False))
        self.server_thread.daemon = True
        self.server_thread.start()

    def wait_for_token(self, timeout=None):
        """
        Wait for the token to be saved with an optional timeout.

        Args:
            timeout (int, optional): Maximum time (in seconds) to wait for the token. Defaults to None (indefinite wait).

        Returns:
            bool: True if the token was saved, False if the wait timed out.
        """
        return self.token_saved_event.wait(timeout)

    def stop_server(self):
        """
        Stop the Flask server by stopping its thread.

        This method is called after the token has been saved or if a timeout occurs.
        """
        if self.server_thread and self.server_thread.is_alive():
            # Flask does not natively support stopping; however, the daemon thread will end with the application.
            print("Stopping authentication server.")
