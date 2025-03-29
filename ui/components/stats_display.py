import tkinter as tk
from typing import Dict

class StatsDisplay(tk.LabelFrame):
    def __init__(self, parent, stats_data: Dict[str, tk.StringVar], **kwargs):
        super().__init__(parent, **kwargs)
        self.stats_vars = stats_data
        self._setup_style()
        self._create_layout()

    def _setup_style(self):
        self.config(
            bg="#f0f0f0",
            font=('Arial', 10, 'bold'),
            relief=tk.GROOVE,
            borderwidth=2,
            labelanchor='n'
        )
        self.label_font = ('Arial', 10)
        self.value_font = ('Arial', 10, 'bold')

    def _create_layout(self):
        # Configure grid
        for i in range(4):
            self.columnconfigure(i, weight=1)

        # Create stats items
        stats_config = [
            ("Games:", self.stats_vars['total_games'], 0, 0),
            ("Player Wins:", self.stats_vars['player_wins'], 0, 2),
            ("AI Wins:", self.stats_vars['ai_wins'], 1, 0),
            ("Avg AI Turn:", self.stats_vars['avg_turn'], 1, 2)
        ]

        for label_text, var, row, col in stats_config:
            self._create_stat_item(label_text, var, row, col)

    def _create_stat_item(self, label_text: str, var: tk.StringVar, row: int, col: int):
        tk.Label(
            self,
            text=label_text,
            bg="#f0f0f0",
            font=self.label_font
        ).grid(row=row, column=col, sticky="w", padx=5)
        
        tk.Label(
            self,
            textvariable=var,
            bg="#f0f0f0",
            font=self.value_font
        ).grid(row=row, column=col+1, sticky="w", padx=5)