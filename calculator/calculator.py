import importlib
from calculator.commands import Command  # Import the Command class for command-based operations

class Calculator:
    def __init__(self):
        self.history = []  # Maintain a history of executed commands
        self.plugins = {}  # Dictionary to store loaded plugins

    def compute(self, command: Command):
        """Execute a command and store it in the history."""
        result = command.execute()  # Execute the provided command
        self.history.append(command)  # Store the command in history
        return result  # Return the result of the command

    def load_plugin(self, plugin_name: str):
        """Dynamically load a plugin by its name from the plugins folder."""
        try:
            # Import the plugin module dynamically from the plugins folder
            plugin_module = importlib.import_module(f"calculator.plugins.{plugin_name}")
            # Register the command class from the plugin
            command_class = plugin_module.register()
            # Store the command class in the plugins dictionary
            self.plugins[plugin_name] = command_class
        except ImportError:
            raise ImportError(f"Failed to load plugin: {plugin_name}")

    def create_command(self, plugin_name: str, *args):
        """Create and return a command from the loaded plugin."""
        # Check if the plugin has been loaded
        if plugin_name in self.plugins:
            # Return an instance of the command class with provided arguments
            return self.plugins[plugin_name](*args)
        else:
            raise ValueError(f"Plugin not found: {plugin_name}")