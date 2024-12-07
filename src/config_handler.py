"""
config_handler.py
------------------
This module provides the `ConfigHandler` class, a utility for managing YAML configuration files
while preserving comments and formatting. It uses the `ruamel.yaml` library to ensure YAML files
maintain their original structure and readability.

Classes:
    - ConfigHandler: Handles loading and saving of YAML configuration files with comment preservation.

Usage:
    The `ConfigHandler` is designed to be integrated into applications that require configuration
    file management. It allows reading, updating, and saving YAML files while retaining their
    comments and formatting.

Dependencies:
    - ruamel.yaml: Provides advanced YAML processing capabilities, including comment preservation.

Example:
    ```python
    from config_handler import ConfigHandler

    config = ConfigHandler()
    data = config.load("config.yaml")
    data["new_key"] = "new_value"
    config.save("config.yaml", data)
    ```
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

from ruamel.yaml import YAML

class ConfigHandler:
    """
    Utility class for loading and saving YAML configurations with comment preservation.
    """

    def __init__(self):
        """
        Initialize the Config handler with ruamel.yaml.
        """
        self.yaml = YAML()
        self.yaml.preserve_quotes = True  # Preserve quotes and formatting

    def load(self, filepath):
        """
        Load a YAML file, preserving comments.

        Args:
            filepath (str): Path to the YAML file.

        Returns:
            dict: Parsed YAML content as a dictionary.
        """
        with open(filepath, 'r') as file:
            return self.yaml.load(file)

    def save(self, filepath, data):
        """
        Save data to a YAML file, preserving comments.

        Args:
            filepath (str): Path to the YAML file.
            data (dict): Data to be saved.
        """
        with open(filepath, 'w') as file:
            self.yaml.dump(data, file)
