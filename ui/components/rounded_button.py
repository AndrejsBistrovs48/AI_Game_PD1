import tkinter as tk

class RoundedButton(tk.Canvas):
    def __init__(self, master=None, text="", radius=10, bg="#95a5a6", fg="white", 
                 activebg="#7f8c8d", command=None, font=('Arial', 10, 'bold'), **kwargs):
        super().__init__(master, highlightthickness=0, **kwargs)
        self.command = command
        self.radius = radius
        self.bg = bg
        self.fg = fg
        self.activebg = activebg
        self.font = font
        
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
        self.text = text
        self.draw_button()
        
    def draw_button(self, bg=None):
        self.delete("all")
        bg = bg if bg else self.bg
        
        # Draw rounded rectangle
        self.create_rounded_rect(0, 0, self.winfo_reqwidth(), self.winfo_reqheight(), 
                                radius=self.radius, fill=bg, outline=bg)
        
        # Add text
        self.create_text(self.winfo_reqwidth()/2, self.winfo_reqheight()/2, 
                        text=self.text, fill=self.fg, font=self.font)
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius=10, **kwargs):
        points = [x1+radius, y1,
                 x1+radius, y1,
                 x2-radius, y1,
                 x2-radius, y1,
                 x2, y1,
                 x2, y1+radius,
                 x2, y1+radius,
                 x2, y2-radius,
                 x2, y2-radius,
                 x2, y2,
                 x2-radius, y2,
                 x2-radius, y2,
                 x1+radius, y2,
                 x1+radius, y2,
                 x1, y2,
                 x1, y2-radius,
                 x1, y2-radius,
                 x1, y1+radius,
                 x1, y1+radius,
                 x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)
    
    def _on_click(self, event):
        if self.command:
            self.command()
    
    def _on_enter(self, event):
        self.draw_button(self.activebg)
    
    def _on_leave(self, event):
        self.draw_button(self.bg)