"""
BigControlCenter - Data Manager utility

This module is responsible for handling data storage in JSON format,
providing a clean interface for saving and loading application data.
"""

import os
import json
from pathlib import Path


class DataManager:
    """Utility class for managing application data in JSON format"""

    def __init__(self, data_dir=None):
        """Initialize the data manager with the specified data directory"""
        if data_dir:
            self.data_dir = Path(data_dir)
        else:
            # Default data directory is ~/.config/bigcontrolcenter
            self.data_dir = Path(os.path.expanduser("~/.config/bigcontrolcenter"))

        # Create the data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)

    def save_data(self, data, filename):
        """
        Save data to a JSON file

        Args:
            data: The data to save (must be JSON serializable)
            filename: The name of the file (without path)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            file_path = self.data_dir / filename
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving data to {filename}: {e}")
            return False

    def load_data(self, filename, default=None):
        """
        Load data from a JSON file

        Args:
            filename: The name of the file (without path)
            default: The default value to return if the file doesn't exist
                    or cannot be loaded

        Returns:
            The loaded data or the default value
        """
        try:
            file_path = self.data_dir / filename
            if not file_path.exists():
                return default

            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading data from {filename}: {e}")
            return default

    def get_categories_data(self):
        """
        Get the categories data, either from a stored file or the default

        Returns:
            list: The categories data
        """
        default_categories = [
            {"name": "Star", "icon": "starred-symbolic", "label": "Main"},
            {
                "name": "Network",
                "icon": "network-wireless-symbolic",
                "label": "Network and Internet",
            },
            {"name": "Phone", "icon": "phone-symbolic", "label": "Phone"},
            {
                "name": "Personalization",
                "icon": "preferences-desktop-appearance-symbolic",
                "label": "Customize",
            },
            {
                "name": "Language",
                "icon": "preferences-desktop-locale-symbolic",
                "label": "Region and Language",
            },
            {
                "name": "Multimedia",
                "icon": "multimedia-volume-control-symbolic",
                "label": "Multimedia",
            },
            {"name": "Account", "icon": "system-users-symbolic", "label": "Accounts"},
            {
                "name": "Hardware",
                "icon": "preferences-system-devices-symbolic",
                "label": "Devices",
            },
            {
                "name": "System",
                "icon": "preferences-system-symbolic",
                "label": "System",
            },
            {"name": "About", "icon": "help-about-symbolic", "label": "About"},
            {"name": "Other", "icon": "applications-other-symbolic", "label": "Other"},
        ]

        return self.load_data("categories.json", default=default_categories)

    def save_categories_data(self, categories):
        """
        Save categories data to a JSON file

        Args:
            categories: The categories data to save

        Returns:
            bool: True if successful, False otherwise
        """
        return self.save_data(categories, "categories.json")

    def get_user_preferences(self):
        """
        Get user preferences, either from a stored file or the default

        Returns:
            dict: The user preferences
        """
        default_preferences = {
            "default_category": "Star",
            "window_width": 1000,
            "window_height": 700,
            "show_descriptions": True,
        }

        return self.load_data("preferences.json", default=default_preferences)

    def save_user_preferences(self, preferences):
        """
        Save user preferences to a JSON file

        Args:
            preferences: The preferences to save

        Returns:
            bool: True if successful, False otherwise
        """
        return self.save_data(preferences, "preferences.json")
