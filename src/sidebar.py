import customtkinter as ckt
from . import config

class Sidebar(ckt.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, width = config.width/4, **kwargs)
        self.pack(side="left", fill="both")
        self.pack_propagate(False)
        
        self.top_margin = ckt.CTkFrame(self, fg_color="transparent", height=40)
        self.top_margin.pack(fill="x")

        self.btn_passwords = ckt.CTkButton(self, text = "🔑 Passwords", font = config.button_font, fg_color="#242424", hover_color="#2b2f36", width=220, height=36, corner_radius=10,  command=lambda: self.select_page("passwords", master))
        self.btn_wallets = ckt.CTkButton(self, text = "$ Crypto Wallets", font = config.button_font, fg_color="#242424", hover_color="#2b2f36", width=220, height=36, corner_radius=10, command=lambda: self.select_page("wallets", master))
        self.btn_settings = ckt.CTkButton(self, text = "⚙️ Settings", font = config.button_font, fg_color="#242424", hover_color="#2b2f36", width=220, height=36, corner_radius=10, command=lambda: self.select_page("settings", master))
        self.spacer = ckt.CTkFrame(self, fg_color="transparent")

        self.nav_buttons = [self.btn_passwords, self.btn_wallets, self.btn_settings]

        self.btn_passwords.pack(padx=12, pady=8, fill="y")
        self.btn_wallets.pack(padx=12, pady=8, fill="y")
        self.spacer.pack(expand = True, fill = "both")
        self.btn_settings.pack(padx=12, pady=8, fill="y")

        self.bottom_margin = ckt.CTkFrame(self, fg_color="transparent", height=40)
        self.bottom_margin.pack(fill="x")

    def select_page(self, page, master):
        # Reset all buttons to the inactive color
        for button in self.nav_buttons:
            button.configure(fg_color=config.INACTIVE_COLOR)

        # Set the active button's color and call the correct content function
        if page == "passwords":
            self.btn_passwords.configure(fg_color=config.ACCENT_COLOR)
            master.content.showPasswords()
        elif page == "wallets":
            self.btn_wallets.configure(fg_color=config.ACCENT_COLOR)
            master.content.showWallets()
        elif page == "settings":
            self.btn_settings.configure(fg_color=config.ACCENT_COLOR)
            master.content.showSettings()