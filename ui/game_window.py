import tkinter as tk
import random
from ui.components.button_factory import ButtonFactory

class GameWindow(tk.Toplevel):
    """Main game window handling gameplay and display"""
    
    def __init__(self, controller, settings):
        super().__init__()
        self.controller = controller
        self.button_factory = ButtonFactory()
        self._init_game_state(settings)
        self._setup_window()
        self.create_widgets()
        self.update_display()
        
        if self.current_player == "Computer":
            self.after(1000, self.ai_move)

    def _init_game_state(self, settings):
        """Initialize game state variables"""
        self.current_number = int(settings['number'])
        self.current_player = str(settings['first_player'])
        self.algorithm = str(settings['algorithm'])
        self.player_score = 0
        self.ai_score = 0
        self.bank = 0

    def _setup_window(self):
        """Configure main window properties"""
        self.title("Number Strategy Game")
        self.geometry("800x600")
        self.config(bg="#f0f0f0")

    def create_widgets(self):
        """Create all UI elements"""
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)

        self._create_score_display(main_frame)
        self._create_number_display(main_frame)
        self._create_action_buttons(main_frame)
        self._create_game_log(main_frame)

    def _create_score_display(self, parent):
        """Create score display widgets"""
        frame = tk.Frame(parent, bg="#f0f0f0")
        frame.pack(fill=tk.X, pady=10)

        # Create score labels
        self.player_score_label = self._create_score_label(frame, "Player Score:", "0")
        self.ai_score_label = self._create_score_label(frame, "AI Score:", "0")
        self.bank_label = self._create_score_label(frame, "Bank:", "0")
        
        # Current player indicator
        self.current_player_label = tk.Label(
            frame, text=f"Current: {self.current_player}", 
            bg="#f0f0f0", font=('Arial', 12, 'italic')
        )
        self.current_player_label.pack(side=tk.RIGHT, padx=10)

    def _create_score_label(self, parent, text, initial_value):
        """Helper to create consistent score labels"""
        tk.Label(parent, text=text, bg="#f0f0f0", font=('Arial', 12)).pack(side=tk.LEFT, padx=10)
        label = tk.Label(parent, text=initial_value, bg="#f0f0f0", font=('Arial', 12, 'bold'))
        label.pack(side=tk.LEFT, padx=5)
        return label

    def _create_number_display(self, parent):
        """Create current number display"""
        self.number_display = tk.Label(
            parent, text="", bg="#f0f0f0", fg="#2c3e50",
            font=('Arial', 36, 'bold')
        )
        self.number_display.pack(pady=20)

    def _create_action_buttons(self, parent):
        """Create container for action buttons"""
        self.actions_frame = tk.Frame(parent, bg="#f0f0f0")
        self.actions_frame.pack(pady=20)

    def _create_game_log(self, parent):
        """Create game log widget"""
        log_frame = tk.LabelFrame(parent, text=" Game Log ", bg="#f0f0f0", font=('Arial', 10))
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.log_text = tk.Text(
            log_frame, height=10, wrap=tk.WORD,
            bg="white", fg="#2c3e50", font=('Arial', 10)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_text.config(state=tk.DISABLED)

    def update_display(self):
        """Update all UI elements to reflect current game state"""
        self.number_display.config(text=str(self.current_number))
        self.player_score_label.config(text=str(self.player_score))
        self.ai_score_label.config(text=str(self.ai_score))
        self.bank_label.config(text=str(self.bank))
        self.current_player_label.config(text=f"Current: {self.current_player}")
        
        if not self.has_valid_moves() or self.current_number <= 10:
            self.end_game()
            return
            
        self.update_action_buttons()
        self.add_log(f"Current number: {self.current_number}")

    def has_valid_moves(self):
        """Check if there are any valid moves remaining"""
        return (self.current_number % 2 == 0) or (self.current_number % 3 == 0)

    def update_action_buttons(self):
        """Dynamically show only valid division buttons"""
        for widget in self.actions_frame.winfo_children():
            widget.destroy()

        if self.current_player == "Player":
            if self.current_number % 2 == 0:
                self.button_factory.create_action_button(
                    self.actions_frame,
                    "Divide by 2",
                    lambda: self.make_move(2)
                ).pack(side=tk.LEFT, padx=10)

            if self.current_number % 3 == 0:
                self.button_factory.create_action_button(
                    self.actions_frame,
                    "Divide by 3",
                    lambda: self.make_move(3)
                ).pack(side=tk.LEFT, padx=10)

    def make_move(self, divisor):
        """Handle player move"""
        new_number = self.current_number // divisor
        
        # Update scores based on divisor
        if divisor == 2:
            self.ai_score += 2
        else:
            self.player_score += 3
        
        # Check for bank bonus
        if new_number % 10 in [0, 5]:
            self.bank += 1
        
        self.current_number = new_number
        self.current_player = "Computer"
        self.update_display()
        self.add_log(f"Player divided by {divisor}")
        
        if self.current_player == "Computer":
            self.after(1000, self.ai_move)

    def ai_move(self):
        """Handle AI move based on selected algorithm"""
        possible_moves = []
        if self.current_number % 2 == 0:
            possible_moves.append(2)
        if self.current_number % 3 == 0:
            possible_moves.append(3)
        
        if not possible_moves:
            self.end_game()
            return
            
        divisor = self._select_ai_move(possible_moves)
        self.process_ai_move(divisor)

    def _select_ai_move(self, possible_moves):
        """Select move based on algorithm"""
        if self.algorithm == "Minimax":
            return self.minimax_ai(possible_moves)
        elif self.algorithm == "Alpha-Beta":
            return self.alphabeta_ai(possible_moves)
        return random.choice(possible_moves)

    def minimax_ai(self, possible_moves):
        """TODO: Implement actual minimax algorithm"""
        return random.choice(possible_moves)

    def alphabeta_ai(self, possible_moves):
        """TODO: Implement actual alpha-beta algorithm"""
        return random.choice(possible_moves)

    def process_ai_move(self, divisor):
        """Process the AI's selected move"""
        new_number = self.current_number // divisor
        
        # Update scores
        if divisor == 2:
            self.ai_score += 2
        else:
            self.player_score += 3
        
        # Check for bank bonus
        if new_number % 10 in [0, 5]:
            self.bank += 1
        
        self.current_number = new_number
        self.current_player = "Player"
        self.update_display()
        self.add_log(f"AI ({self.algorithm}) divided by {divisor}")

    def end_game(self):
        """Handle game end conditions"""
        # Add bank to current player's score
        if self.current_player == "Player":
            self.player_score += self.bank
        else:
            self.ai_score += self.bank
        
        self.bank = 0
        
        # Determine winner
        if self.player_score > self.ai_score:
            winner = "Player wins!"
        elif self.ai_score > self.player_score:
            winner = "AI wins!"
        else:
            winner = "It's a tie!"
        
        # Update final display
        self.number_display.config(text=str(self.current_number))
        self.player_score_label.config(text=str(self.player_score))
        self.ai_score_label.config(text=str(self.ai_score))
        self.bank_label.config(text=str(self.bank))
        
        self.add_log(f"Game over! Final number: {self.current_number}")
        self.add_log(f"Final scores - Player: {self.player_score}, AI: {self.ai_score}")
        self.add_log(winner)
        
        # Clear and show restart button
        for widget in self.actions_frame.winfo_children():
            widget.destroy()
        
        self.button_factory.create_restart_button(
            self.actions_frame,
            self.return_to_settings
        ).pack(side=tk.LEFT, padx=10)

    def add_log(self, message):
        """Add message to game log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)

    def return_to_settings(self):
        """Return to settings window"""
        self.destroy()
        self.controller.show_settings()