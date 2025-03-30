import tkinter as tk
from collections import deque

class AppController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window
        
        self.settings_window = None
        self.game_window = None
        
         # Statistics tracking
        self.game_stats = {
            'total_games': 0,
            'player_wins': 0,
            'ai_wins': 0,
            'ai_turn_times': deque(maxlen=10),  # Stores last 10 turn times,
            'nodes_visited': 0
        }

        self.show_settings()

    def record_game_result(self, winner):
        #Record the outcome of a completed game#
        self.game_stats['total_games'] += 1
        if winner == "Player":
            self.game_stats['player_wins'] += 1
        elif winner == "AI":
            self.game_stats['ai_wins'] += 1
        
        # Update statistics in settings window
        if self.settings_window:
            self.settings_window.update_stats_display()
            self.settings_window.update() 

    def record_ai_turn_time(self, turn_time, nodes_visited):
        #Record time taken for AI to complete a turn#
        self.game_stats['ai_turn_times'].append(turn_time)
        self.game_stats['nodes_visited'] = self.game_stats['nodes_visited'] + nodes_visited
        # print(str(self.game_stats['nodes_visited']) + " | " + str(nodes_visited))
        if self.settings_window:
            self.settings_window.update_stats_display()

    def show_settings(self):
        #Show the settings window and hide others#
        if self.game_window:
            self.game_window.destroy()
            
        from ui.settings_window import SettingsWindow  # Import here to avoid circular imports
        self.settings_window = SettingsWindow(self)
        self.settings_window.deiconify()

    def start_game(self, settings):
        #Start the game with given settings#
        if self.settings_window:
            self.settings_window.withdraw()
            
        from ui.game_window import GameWindow  # Import here to avoid circular imports
        self.game_window = GameWindow(self, settings)
        
    def run(self):
        #Start the main application loop#
        self.root.mainloop()

if __name__ == "__main__":
    controller = AppController()
    controller.run()