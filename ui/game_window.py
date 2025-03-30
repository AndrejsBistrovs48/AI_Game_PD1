import sys
sys.path.append('game')
sys.path.append('game/ui')

import tkinter as tk
import time

from ui.components.button_factory import ButtonFactory

from game.tree_builders.minimax_node import MiniMaxTreeNode
from game.tree_builders.alphabeta_node import AlphaBetaTreeNode

class GameWindow(tk.Toplevel):
    #Main game window handling gameplay and display
    
    def __init__(self, controller, settings):
        super().__init__()
        self.controller = controller
        self.button_factory = ButtonFactory()
        self._init_game_state(settings)
        self._setup_window()
        self.create_widgets()
        self.update_display()
        self.ai_move_start_time = None 
        self.add_log("Starting the game. Chosen number: " + str(self.tree_node.number))
        
        if not self.tree_node.p1_turn:
            self.after(1000, self.ai_move)

    def _init_game_state(self, settings):
        #Initialize game state variables
        self.algorithm = str(settings['algorithm'])

        TreeClass = MiniMaxTreeNode if self.algorithm == "Minimax" else AlphaBetaTreeNode # initializing tree
        self.tree_node = TreeClass(int(settings['number']), str(settings['first_player']) == 'Player')

    def _setup_window(self):
        #Configure main window properties
        self.title("Number Strategy Game")
        self.geometry("800x600")
        self.config(bg="#f0f0f0")

    def create_widgets(self):
        #Create all UI elements
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)

        self._create_score_display(main_frame)
        self._create_number_display(main_frame)
        self._create_action_buttons(main_frame)
        self._create_game_log(main_frame)

    def _create_score_display(self, parent):
        #Create score display widgets
        frame = tk.Frame(parent, bg="#f0f0f0")
        frame.pack(fill=tk.X, pady=10)

        # Create score labels
        self.player_score_label = self._create_score_label(frame, "Player Score:", "0")
        self.ai_score_label = self._create_score_label(frame, "AI Score:", "0")
        self.bank_label = self._create_score_label(frame, "Bank:", "0")
        
        # Current player indicator
        self.current_player_label = tk.Label(
            frame, text=f"Current: {'Player' if self.tree_node.p1_turn else 'Computer'}", 
            bg="#f0f0f0", font=('Arial', 12, 'italic')
        )
        self.current_player_label.pack(side=tk.RIGHT, padx=10)

    def _create_score_label(self, parent, text, initial_value):
        # Helper to create consistent score labels
        tk.Label(parent, text=text, bg="#f0f0f0", font=('Arial', 12)).pack(side=tk.LEFT, padx=10)
        label = tk.Label(parent, text=initial_value, bg="#f0f0f0", font=('Arial', 12, 'bold'))
        label.pack(side=tk.LEFT, padx=5)
        return label

    def _create_number_display(self, parent):
        #Create current number display
        self.number_display = tk.Label(
            parent, text="", bg="#f0f0f0", fg="#2c3e50",
            font=('Arial', 36, 'bold')
        )
        self.number_display.pack(pady=20)

    def _create_action_buttons(self, parent):
        #Create container for action buttons
        self.actions_frame = tk.Frame(parent, bg="#f0f0f0")
        self.actions_frame.pack(pady=20)

    def _create_game_log(self, parent):
        #Create game log widget
        log_frame = tk.LabelFrame(parent, text=" Game Log ", bg="#f0f0f0", font=('Arial', 10))
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.log_text = tk.Text(
            log_frame, height=10, wrap=tk.WORD,
            bg="white", fg="#2c3e50", font=('Arial', 10)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_text.config(state=tk.DISABLED)

    def update_display(self):
        #Update UI elements to reflect current game state
        node = self.tree_node
        self.number_display.config(text=str(node.number))
        self.player_score_label.config(text=str(node.scores[0]))
        self.ai_score_label.config(text=str(node.scores[1]))
        self.bank_label.config(text=str(node.bank))
        self.current_player_label.config(text=f"Current: {'Player' if node.p1_turn else 'Computer'}")
            
        self.update_action_buttons()

    def update_action_buttons(self):
        #Show only valid division buttons
        for widget in self.actions_frame.winfo_children():
            widget.destroy()

        if self.tree_node.p1_turn:
            if self.tree_node.divide_by_2 is not None:
                self.button_factory.create_action_button(
                    self.actions_frame,
                    "Divide by 2",
                    lambda: self.make_move(2)
                ).pack(side=tk.LEFT, padx=10)

            if self.tree_node.divide_by_3 is not None:
                self.button_factory.create_action_button(
                    self.actions_frame,
                    "Divide by 3",
                    lambda: self.make_move(3)
                ).pack(side=tk.LEFT, padx=10)

    def make_move(self, divisor):
        #Handle player move
        self.tree_node = self.tree_node.divide_by_2 if divisor == 2 else self.tree_node.divide_by_3
        
        self.update_display()
        self.add_log(f"Player divided by {divisor}. New number: {self.tree_node.number}")
        
        self.after(1000, self.ai_move)

    def ai_move(self):
        #Handle AI move and track time based on selected algorithm
        self.ai_move_start_time = time.time()
        if self.tree_node.finished:
            self.end_game()
            return
        
        best_node, node_count, time_taken = self.tree_node.algorithm()
        
        if best_node is None:
            self.end_game()
            return
            
        divisor = self.tree_node.number // best_node.number

        self.tree_node = best_node

        if best_node.finished:
            self.end_game()
            return
        
        self.controller.record_ai_turn_time(time_taken, node_count)
        self.update_display()
        self.add_log(f"AI ({self.algorithm}) divided by {divisor}. New number: {self.tree_node.number}")
        self.add_log(f"     Stats: AI visited {node_count} nodes and it took {time_taken} nanoseconds")

    def end_game(self):
        #Handle game end conditions
        
        player_score = self.tree_node.scores[0]
        ai_score = self.tree_node.scores[1]

        # Determine winner
        if player_score > ai_score:
            winner = "Player"
            result_text = "Player wins!"
        elif ai_score > player_score:
            winner = "AI"
            result_text = "AI wins!"
        else:
            winner = "Tie"
            result_text = "It's a tie!"

        self.controller.record_game_result(winner)
        # Update final display
        self.number_display.config(text=str(self.tree_node.number))
        self.player_score_label.config(text=str(player_score))
        self.ai_score_label.config(text=str(ai_score))
        self.bank_label.config(text=str(self.tree_node.bank))
        
        self.add_log(f"Game over! Final number: {self.tree_node.number}")
        self.add_log(f"Final scores - Player: {player_score}, AI: {ai_score}")
        self.add_log(result_text)
        
        # Clear and show restart button
        for widget in self.actions_frame.winfo_children():
            widget.destroy()
        
        self.button_factory.create_restart_button(
            self.actions_frame,
            self.return_to_settings
        ).pack(side=tk.LEFT, padx=10)

    def add_log(self, message):
        #Add message to game log
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)

    def return_to_settings(self):
        #Return to settings window
        self.destroy()
        self.controller.show_settings()
        self.controller.settings_window.update_stats_display()