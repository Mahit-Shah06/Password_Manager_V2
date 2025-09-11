import customtkinter as ckt
from . import config
from .auth_screen import AuthScreen
from .sidebar import Sidebar
from .content_area import ContentArea

class GUI(ckt.CTk):
    def __init__(self):
        super().__init__()

        self.geometry(f"{config.width}x{config.height}")
        self.minsize(config.width/2, config.height/2)
        self.title("Password Manager")

        self.current_frame = None
        self.start_auth_screen()

    def start_auth_screen(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = AuthScreen(self) 
        self.current_frame.pack(fill="both", expand=True)

    def show_main_app(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = ckt.CTkFrame(self, fg_color="transparent")
        self.current_frame.pack(fill="both", expand=True)

        self.content = ContentArea(self.current_frame)
        self.sidebar = Sidebar(self.current_frame)
        self.current_frame.content = self.content

        self.sidebar.select_page("passwords", self.current_frame)