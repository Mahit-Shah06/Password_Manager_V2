import customtkinter as ckt
from . import config
from . import db
from . import encryption_logic
from . import session_handler

class ContentArea(ckt.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color = "transparent", width = 3*config.width/4, **kwargs)
        self.pack(side = "right", fill = "both")
        self.pack_propagate(False)

        self.inner_frame = ckt.CTkFrame(self, fg_color="transparent")
        self.inner_frame.pack(side="left", fill = 'both', expand="True", padx=30, pady=20)
        self.dbf = db.DBfunc()
        self.enc = encryption_logic.EncryptionHandler()
        self.uuid = None
        self.key = None
        self.sh = session_handler.SessionHandler()

    def showPasswords(self):
        self.clear()
        label = ckt.CTkLabel(self.inner_frame, text="Passwords", font=config.text_font)
        label.grid(row=0, column=0, sticky="w")

        search = ckt.CTkEntry(self.inner_frame, placeholder_text="Search...", width=300, font = config.search_font)
        search.grid(row=0, column=2, sticky="e", padx = 20)

        self.inner_frame.grid_columnconfigure(1, weight=1)
        self.inner_frame.grid_columnconfigure(2, weight=0)

        self.Scroller(True, self.inner_frame)

    def showWallets(self):
        self.clear()
        label = ckt.CTkLabel(self.inner_frame, text="Wallets", font=config.text_font)
        label.grid(row=0, column=0, sticky="w")

        search = ckt.CTkEntry(self.inner_frame, placeholder_text="Search...", width=300, font = config.search_font)
        search.grid(row=0, column=2, sticky="e", padx=20)

        self.inner_frame.grid_columnconfigure(0, weight=0)
        self.inner_frame.grid_columnconfigure(1, weight=1)
        self.inner_frame.grid_columnconfigure(2, weight=0)

        self.Scroller(False, self.inner_frame)

    def Scroller(self, type, frame):
        self.clear()
        scroll_frame = ckt.CTkScrollableFrame(frame, width=600, height=400)
        scroll_frame.grid(row=1, column=0, columnspan=3, pady=20, sticky="nsew")

        if type is True:
            self.uuid, self.key = self.sh.load_session()

            entries = self.dbf.retrieve_passwords(self.uuid)
            print(entries)
            for site, username, enc_pass, notes in entries:
                try:
                    decrypted_pass = self.enc.decrypt(enc_pass)
                except Exception:
                    decrypted_pass = "<decryption failed>"

                inframe = ckt.CTkFrame(scroll_frame, corner_radius=10)
                inframe.pack(fill="x", pady=5, padx=10)

                label = ckt.CTkLabel(inframe, text=f"{site} \n {username}", anchor="w")
                label.pack(side="left", padx=10, pady=5)

                pass_var = ckt.StringVar(value="••••••••")
                pass_label = ckt.CTkLabel(inframe, textvariable=pass_var, width=150, anchor="w")
                pass_label.pack(side="left", padx=10, pady=5)

                def toggle(var=pass_var, real=decrypted_pass):
                    if var.get() == "••••••••":
                        var.set(real)
                    else:
                        var.set("••••••••")

                show_chk = ckt.CTkCheckBox(inframe, text="Show", command=toggle)
                show_chk.pack(side="right", padx=10)

    def add(self, frame):
        pass

    def showSettings(self):
        self.clear()
        label = ckt.CTkLabel(self.inner_frame, text="Settings", font=config.text_font)
        label.grid(row=0, column=0, sticky="w")

    def clear(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()