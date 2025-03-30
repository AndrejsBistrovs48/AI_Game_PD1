import tkinter as tk
from tkinter import messagebox
from game.utils.number_generator import generate_initial_numbers
from ui.components.button_factory import ButtonFactory
from ui.components.settings_section import SettingsSection
from ui.components.stats_display import StatsDisplay

class SettingsWindow(tk.Toplevel):
    #Game settings configuration window
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.button_factory = ButtonFactory()
        self.settings = {
            'first_player': None,
            'algorithm': None,
            'number': None
        }
        
        self._setup_window()
        self.create_widgets()
        self._create_stats_display() 
        self.generate_numbers()

    def _setup_window(self):
        #Configure settings/main window properties
        self.title("Game Settings")
        self.geometry("700x600")
        self.config(bg="#f0f0f0")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        #Create UI elements
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)

        # Create settings sections
        self._create_settings_sections(main_frame)
        self._create_start_button(main_frame)

    def _create_settings_sections(self, parent):
        #Create the three settings sections
        self.player_section = SettingsSection(
            parent, "1. Who Starts the Game",
            ["Player", "Computer"], 'first_player', self.update_setting
        )
        self.player_section.pack(fill=tk.X, pady=10)
        
        self.number_section = SettingsSection(
            parent, "2. Select Starting Number",
            [], 'number', self.update_setting
        )
        self.number_section.pack(fill=tk.X, pady=10)
        
        self.algorithm_section = SettingsSection(
            parent, "3. Choose AI Algorithm",
            ["Minimax", "Alpha-Beta"], 'algorithm', self.update_setting
        )
        self.algorithm_section.pack(fill=tk.X, pady=10)

    def _create_start_button(self, parent):
        #Create the start game button
        self.start_btn = self.button_factory.create_start_button(
            parent, self.start_game
        )
        self.start_btn.pack(pady=20)

    def _create_stats_display(self):
        #Create clean statistics display using component
        self.stats_vars = {
            'total_games': tk.StringVar(value="0"),
            'player_wins': tk.StringVar(value="0"),
            'ai_wins': tk.StringVar(value="0"),
            'avg_turn': tk.StringVar(value="No data"),
            'nodes_visited': tk.StringVar(value="0")
        }
        
        self.stats_display = StatsDisplay(
            self,
            stats_data=self.stats_vars,
            text=" Game Statistics "
        )
        self.stats_display.pack(fill=tk.X, padx=40, pady=(0, 20))

    def update_stats_display(self):
        #Update stats display with current data
        stats = self.controller.game_stats
        self.stats_vars['total_games'].set(str(stats['total_games']))
        self.stats_vars['player_wins'].set(str(stats['player_wins']))
        self.stats_vars['ai_wins'].set(str(stats['ai_wins']))
        
        # Calculate average turn time
        if stats['ai_turn_times']:
            avg_time = sum(stats['ai_turn_times']) / len(stats['ai_turn_times'])
            self.stats_vars['avg_turn'].set(f"{avg_time:.2f}s")
        else:
            self.stats_vars['avg_turn'].set("No data")

        # Calculate total visited nodes
        self.stats_vars['nodes_visited'].set(stats['nodes_visited'])

    def generate_numbers(self):
        #Generate valid starting numbers
        try:
            numbers = generate_initial_numbers()
            for num in numbers:
                self.number_section.add_option(num)
        except Exception as e:
            messagebox.showerror("Error", f"Number generation failed: {str(e)}")
            self.controller.show_settings()

    def update_setting(self, key, value):
        #Update setting and check if all are complete
        self.settings[key] = value
        self.check_completeness()

    def check_completeness(self):
        #Enable start button only when all settings are selected 
        if all(self.settings.values()):
            self.start_btn.bg = "#27ae60"
            self.start_btn.activebg = "#219a52"
            self.start_btn.draw_button()
        else:
            self.start_btn.bg = "#e74c3c"
            self.start_btn.activebg = "#c0392b"
            self.start_btn.draw_button()

    def start_game(self):
        #Validate settings and start the game
        if not all(self.settings.values()):
            messagebox.showwarning(
                "Incomplete Settings",
                "Please select all options before starting the game"
            )
            return
        
        #
        self.settings['number'] = int(self.settings['number'])
        self.controller.start_game(self.settings)

    def on_close(self):
        #Handle window close event
        self.controller.root.quit()

    def destroy(self):
        #Override destroy to properly close application
        self.controller.root.quit()
        super().destroy()