from ui.components.rounded_button import RoundedButton

class ButtonFactory:
    """Factory for creating consistent buttons throughout the application"""
    
    #  button styles
    _ACTION_STYLE = {
        'radius': 8,
        'bg': "#5d6d7e",
        'fg': "white",
        'activebg': "#4a5a6b",
        'font': ('Arial', 12, 'bold'),
        'width': 120,
        'height': 45
    }
    
    _RESTART_STYLE = {
        'radius': 8,
        'bg': "#27ae60",
        'fg': "white",
        'activebg': "#219a52",
        'font': ('Arial', 12, 'bold'),
        'width': 120,
        'height': 45
    }
    
    _START_STYLE = {
        'radius': 10,
        'bg': "#e74c3c",
        'fg': "white",
        'activebg': "#c0392b",
        'font': ('Arial', 12, 'bold'),
        'width': 150,
        'height': 40
    }

    @classmethod
    def create_action_button(cls, master, text, command):
        """Create a standard action button"""
        return RoundedButton(
            master=master,
            text=text,
            command=command,
            **cls._ACTION_STYLE
        )

    @classmethod
    def create_restart_button(cls, master, command):
        """Create a restart game button"""
        return RoundedButton(
            master=master,
            text="Play Again",
            command=command,
            **cls._RESTART_STYLE
        )

    @classmethod
    def create_start_button(cls, master, command):
        """Create a start game button"""
        return RoundedButton(
            master=master,
            text="Start Game",
            command=command,
            **cls._START_STYLE
        )