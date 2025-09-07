import customtkinter as ckt
from . import config
from . import db
from . import encryption_logic

class ContentArea(ckt.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color = "transparent", width = 3*config.width/4, **kwargs)
        self.pack(side = "right", fill = "both")
        self.pack_propagate(False)

        self.inner_frame = ckt.CTkFrame(self, fg_color="transparent")
        self.inner_frame.pack(side="left", fill = 'both', expand="True", padx=30, pady=20)
        self.dbf = db.DBfunc()
        self.enc = encryption_logic.EncryptionHandler()

    def showPasswords(self):
        self.clear()
        label = ckt.CTkLabel(self.inner_frame, text="Passwords", font=config.text_font)
        label.grid(row=0, column=0, sticky="w")

        search = ckt.CTkEntry(self.inner_frame, placeholder_text="Search...", width=300, font = config.search_font)
        search.grid(row=0, column=2, sticky="e", padx = 20)

        self.inner_frame.grid_columnconfigure(1, weight=1)
        self.inner_frame.grid_columnconfigure(2, weight=0)

    def showWallets(self):
        self.clear()
        label = ckt.CTkLabel(self.inner_frame, text="Wallets", font=config.text_font)
        label.grid(row=0, column=0, sticky="w")

        search = ckt.CTkEntry(self.inner_frame, placeholder_text="Search...", width=300, font = config.search_font)
        search.grid(row=0, column=2, sticky="e", padx=20)

        self.inner_frame.grid_columnconfigure(0, weight=0)
        self.inner_frame.grid_columnconfigure(1, weight=1)
        self.inner_frame.grid_columnconfigure(2, weight=0)

    def Scroller(self):
        pass

    def showSettings(self):
        self.clear()
        label = ckt.CTkLabel(self.inner_frame, text="Settings", font=config.text_font)
        label.grid(row=0, column=0, sticky="w")

    def clear(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

# Demo data
# DEMO_PASSWORDS = [
#     {"site": "github.com", "username": "you@example.com", "password": "••••••••"},
#     {"site": "gmail.com",  "username": "you@gmail.com",  "password": "••••••••"},
#     {"site": "notion.so",  "username": "you@work.com",  "password": "••••••••"},
# ]

# DEMO_WALLETS = [
#     {"chain": "Ethereum", "label": "Main Wallet", "seed phrase": "satoshi...orbit satoshi"},
#     {"chain": "Solana",   "label": "Cold Storage", "seed phrase": "0x4...b8c8f6f0"},
# ]