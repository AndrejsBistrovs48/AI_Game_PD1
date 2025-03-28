import tkinter as tk

class AppController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window
        
        self.settings_window = None
        self.game_window = None
        
        self.show_settings()

    def show_settings(self):
        """Show the settings window and hide others"""
        if self.game_window:
            self.game_window.destroy()
            
        from ui.settings_window import SettingsWindow  # Import here to avoid circular imports
        self.settings_window = SettingsWindow(self)
        self.settings_window.deiconify()

    def start_game(self, settings):
        """Start the game with given settings"""
        if self.settings_window:
            self.settings_window.withdraw()
            
        from ui.game_window import GameWindow  # Import here to avoid circular imports
        self.game_window = GameWindow(self, settings)
        
    def run(self):
        """Start the main application loop"""
        self.root.mainloop()

if __name__ == "__main__":
    controller = AppController()
    controller.run()