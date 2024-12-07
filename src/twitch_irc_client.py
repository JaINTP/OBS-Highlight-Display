"""
twitch_irc_client.py
---------------------
This module defines the TwitchIRCClient class, which serves as a Twitch bot
for monitoring chat messages and broadcasting specific events to a frontend
via Flask-SocketIO.

Classes:
    - TwitchIRCClient: A Twitch chat bot that integrates with Flask-SocketIO
      to send real-time updates to a connected frontend.
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

from twitchio.ext import commands
from flask_socketio import SocketIO
import requests


class TwitchIRCClient(commands.Bot):
    """
    Represents a Twitch IRC bot that monitors chat messages and communicates
    with a frontend using Flask-SocketIO.

    Attributes:
        config (dict): Configuration dictionary with Twitch and application settings.
        socketio (SocketIO): Flask-SocketIO instance for real-time communication.
    """

    def __init__(self, config, socketio: SocketIO):
        """
        Initialize the Twitch IRC client.

        Args:
            config (dict): Configuration dictionary containing access tokens and other settings.
            socketio (SocketIO): Flask-SocketIO instance for emitting events to the frontend.
        """
        super().__init__(
            token=config['access_token'],
            prefix='!',
            initial_channels=[self.get_user_name(config['access_token'])]
        )
        self.config = config
        self.socketio = socketio  # Flask-SocketIO instance

    def get_user_name(self, token):
        """
        Retrieve the Twitch username associated with the provided access token.

        Args:
            token (str): The OAuth access token.

        Returns:
            str: The username associated with the token.

        Raises:
            Exception: If the token validation fails.
        """
        url = 'https://id.twitch.tv/oauth2/validate'
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()['login']
        else:
            raise Exception("Failed to validate token and retrieve username.")

    async def event_ready(self):
        """
        Handle the event when the bot connects to Twitch chat successfully.
        """
        print(f"Logged in as | {self.nick}")
        print(f"User ID is | {self.user_id}")

    async def event_message(self, message):
        """
        Handle incoming chat messages.

        Args:
            message: TwitchIO message object representing a chat message.
        """
        # Determine if the bot should process its own messages
        process_own_messages = self.config.get('process_own_messages', False)

        # Ignore messages from the bot itself if not allowed
        if not process_own_messages and message.author.name.lower() == self.nick.lower():
            return

        print(f"Message received from {message.author.display_name}: {message.content}")

        # Check if the authenticated user's nickname is mentioned
        authenticated_user = self.nick.lower()
        is_mention = f"@{authenticated_user}" in message.content.lower()
        allow_non_mentions = self.config.get('allow_non_mentions', False)
        is_highlight = is_mention or (allow_non_mentions and authenticated_user in message.content.lower())

        if is_highlight:
            # Emit the message data to the frontend via Flask-SocketIO
            try:
                self.socketio.emit(
                    'update_list',
                    {
                        'username': message.author.display_name,
                        'username_colour': message.author.color,
                        'message': message.content,
                        'timeout': self.config.get('highlight_timeout', 5000)  # Default to 5000 ms if not set
                    },
                    namespace='/'
                )
            except Exception as e:
                print(f"Error emitting message to Flask-SocketIO: {e}")

    async def event_command_error(self, ctx, error):
        """
        Handle errors raised by commands.

        Args:
            ctx: The context of the command.
            error: The error that occurred.
        """
        print(f"An error occurred: {error}")

    def run_bot(self):
        """
        Start the bot's event loop.
        """
        self.run()
