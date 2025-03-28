import tkinter as tk
from .rounded_button import RoundedButton

class SettingsSection(tk.Frame):
    def __init__(self, parent, title, options, setting_key, on_select):
        super().__init__(parent, bg="#f0f0f0")
        self.on_select = on_select
        self.setting_key = setting_key
        self.buttons = []
        
        tk.Label(self, text=title, bg="#f0f0f0", fg="#2c3e50",
               font=('Arial', 11, 'bold')).pack(pady=5)
        
        self.btn_frame = tk.Frame(self, bg="#f0f0f0")
        self.btn_frame.pack()
        
        for option in options:
            self.add_option(option)
    
    def add_option(self, option):
        btn = RoundedButton(
            self.btn_frame,
            text=str(option),
            radius=8,
            bg="#5d6d7e",
            fg="white",
            activebg="#4a5a6b",
            command=lambda v=option: self.select_option(v),
            font=('Arial', 10, 'bold'),
            width=100,
            height=35
        )
        btn.pack(side=tk.LEFT, padx=5, pady=2)
        btn.bind("<Button-1>", lambda e, b=btn: self.handle_selection(b))
        self.buttons.append(btn)
    
    def handle_selection(self, button):
        for btn in self.buttons:
            btn.bg = "#5d6d7e"
            btn.draw_button()
        button.bg = "#219a52"
        button.draw_button()
        self.select_option(button.text)
    
    def select_option(self, value):
        self.on_select(self.setting_key, value)