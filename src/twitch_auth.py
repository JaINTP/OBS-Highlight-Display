"""
twitch_auth.py
--------------
This module defines the TwitchAuth class, responsible for managing the 
OAuth2 flow and token validation/refresh processes for the Twitch API.

Classes:
    - TwitchAuth: Handles the authorization process, token exchange, 
      validation, and refresh operations for Twitch API integration.
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

import requests


class TwitchAuth:
    """
    Manages OAuth2 authentication and token handling for Twitch API.

    Attributes:
        AUTH_URL (str): The Twitch OAuth2 authorization URL.
        TOKEN_URL (str): The Twitch token exchange URL.
        CLIENT_ID (str): The client ID of the application.
        REDIRECT_URI (str): The redirect URI for the application.
    """

    def __init__(self, config):
        """
        Initialize the TwitchAuth instance with the provided configuration.

        Args:
            config (dict): A dictionary containing application settings such as
                           client ID, redirect URI, and endpoint URLs.
        """
        self.AUTH_URL = config['auth_url']
        self.TOKEN_URL = config['token_url']
        self.CLIENT_ID = config['client_id']
        self.REDIRECT_URI = config['redirect_uri']

    def get_auth_initiation_page(self):
        """
        Generate an HTML page for the initial authorization request.

        Returns:
            str: A simple HTML string for the authorization page.
        """
        return f"<html>... Authorization page content ...</html>"

    def exchange_code_for_token(self, code):
        """
        Exchange an authorization code for an access token.

        Args:
            code (str): The authorization code received from Twitch.

        Returns:
            dict or None: A dictionary containing token data if successful, 
                          or None if the exchange fails.
        """
        data = {
            'client_id': self.CLIENT_ID,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.REDIRECT_URI
        }
        response = requests.post(self.TOKEN_URL, data=data)
        if response.status_code == 200:
            return response.json()
        return None

    def validate_token(self, access_token):
        """
        Validate an existing access token.

        Args:
            access_token (str): The access token to validate.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('https://id.twitch.tv/oauth2/validate', headers=headers)
        return response.status_code == 200

    def refresh_token(self, refresh_token):
        """
        Refresh an expired access token using a refresh token.

        Args:
            refresh_token (str): The refresh token.

        Returns:
            dict or None: A dictionary containing the new access token and 
                          refresh token if successful, or None if the refresh fails.
        """
        data = {
            'client_id': self.CLIENT_ID,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        response = requests.post(self.TOKEN_URL, data=data)
        if response.status_code == 200:
            return response.json()
        return None
