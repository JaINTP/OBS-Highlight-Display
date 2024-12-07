"""
main.py
-------
The entry point for the Twitch SignalR application. This script manages the initialization
and orchestration of different components, including authentication, web server, and IRC client.

Classes:
    - Application: Main application class that loads configuration, handles authentication,
      and manages the lifecycle of the web server and Twitch IRC client.

Functions:
    - __main__: Initializes and starts the application.
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

import webbrowser
import threading
from os import path
from auth_server import AuthServer
from web_server import WebServer
from twitch_irc_client import TwitchIRCClient
from twitch_auth import TwitchAuth
from config_handler import ConfigHandler


class Application:
    """
    The main application class for the Twitch SignalR app.

    Attributes:
        config (dict): Application configuration loaded from `config.yaml`.
        auth_server (AuthServer): Handles Twitch OAuth authentication flow.
        web_server (WebServer): Serves the frontend and manages WebSocket communication.
        irc_client (TwitchIRCClient): Handles Twitch chat interactions and emits events to the frontend.
        twitch_auth (TwitchAuth): Handles token management and validation.
    """

    def __init__(self):
        """
        Initializes the application by loading the configuration and creating instances
        of required components.
        """
        base_dir = path.dirname(path.abspath(__file__))
        self.config_path = path.join(base_dir, '..', 'config.yaml')
        self.config_handler = ConfigHandler()
        self.config = self.config_handler.load(self.config_path)
        
        self.auth_server = AuthServer(self.config, self.config_handler)
        self.web_server = WebServer(self.config)
        self.twitch_auth = TwitchAuth(self.config)
        self.irc_client = None  # Defer initialization until token validation

    def save_config(self):
        """
        Save the updated configuration back to `config.yaml`.
        """
        self.yaml_handler.save(self.config_path, self.config)

    def check_auth_token(self):
        """
        Validates or refreshes the access token. If no token is available or the token
        is invalid, it starts the authentication flow.

        Returns:
            bool: True if a valid token is available, False otherwise.
        """
        if self.config.get('access_token') and self.twitch_auth.validate_token(self.config['access_token']):
            print("Valid access token found. Skipping authentication.")
            return True

        if not self.config.get('access_token'):
            print("No valid access token found. Starting authentication flow...")
            webbrowser.open(f"{self.twitch_auth.AUTH_URL}?client_id={self.twitch_auth.CLIENT_ID}&redirect_uri={self.twitch_auth.REDIRECT_URI}&response_type=token&scope=chat:read+chat:edit")
            print(f"Please authenticate via the browser.")
            self.auth_server.start_server()
            return False

        if not self.twitch_auth.validate_token(self.config['access_token']):
            print("Access token is invalid or expired. Attempting to refresh...")
            new_tokens = self.twitch_auth.refresh_token(self.config['refresh_token'])
            if not new_tokens:
                print("Failed to refresh token. Please authenticate again.")
                self.config['access_token'] = None
                self.save_config()
                return self.check_auth_token()

            self.config['access_token'] = new_tokens['access_token']
            self.config['refresh_token'] = new_tokens.get('refresh_token', self.config['refresh_token'])
            self.save_config()
            print("Token refreshed successfully.")

        return True

    def initialize_irc_client(self):
        """
        Initializes the Twitch IRC client after a valid token is confirmed.
        """
        print("Initializing IRC client...")
        self.irc_client = TwitchIRCClient(self.config, self.web_server.socketio)

    def start_irc_client(self):
        """
        Starts the Twitch IRC client in its own thread.
        """
        print("Starting IRC client...")
        self.irc_client.run_bot()

    def run(self):
        """
        Starts the application by validating the token, initializing the IRC client,
        running the web server, and starting the IRC client in a separate thread.
        """
        if not self.check_auth_token():
            print("Starting authentication server...")
            self.auth_server.start_server()

            # Wait for token to be saved or timeout after 60 seconds
            if self.auth_server.wait_for_token(timeout=60):
                print("Token saved successfully.")
            else:
                print("Authentication timed out. Please try again.")

            self.auth_server.stop_server()

        # Initialize IRC client after token validation
        self.initialize_irc_client()

        print("Starting application...")
        # Run the IRC bot in a separate thread
        irc_thread = threading.Thread(target=self.start_irc_client, daemon=True)
        irc_thread.start()

        # Run the Flask web server
        self.web_server.run()


if __name__ == '__main__':
    # Entry point for the application
    app = Application()
    app.run()
