import customtkinter as ckt
from tkinter import messagebox as mb
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
        self.add_entry_fields = {}
        self.uuid, self.key = self.sh.load_session()

    def showPasswords(self):
        self.clear()
        label = ckt.CTkLabel(self.inner_frame, text="Passwords", font=config.text_font)
        label.grid(row=0, column=0, sticky="w")

        search = ckt.CTkEntry(self.inner_frame, placeholder_text="Search...", width=300, font = config.search_font)
        search.grid(row=0, column=2, sticky="e", padx = 20)

        self.inner_frame.grid_columnconfigure(1, weight=1)
        self.inner_frame.grid_columnconfigure(2, weight=0)

        self.Scroller(True)

    def showWallets(self):
        self.clear()
        label = ckt.CTkLabel(self.inner_frame, text="Wallets", font=config.text_font)
        label.grid(row=0, column=0, sticky="w")

        search = ckt.CTkEntry(self.inner_frame, placeholder_text="Search...", width=300, font = config.search_font)
        search.grid(row=0, column=2, sticky="e", padx=20)

        self.inner_frame.grid_columnconfigure(0, weight=0)
        self.inner_frame.grid_columnconfigure(1, weight=1)
        self.inner_frame.grid_columnconfigure(2, weight=0)

        self.Scroller(False)

    def Scroller(self, type):
        add_frame = ckt.CTkFrame(self.inner_frame, corner_radius=10)
        add_frame.grid(row=1, column=0, pady=(20, 0), sticky="ew")

        self.add_entry_fields["site"] = ckt.CTkEntry(add_frame, placeholder_text="Site", width=150)
        self.add_entry_fields["username_email"] = ckt.CTkEntry(add_frame, placeholder_text="Username/Email", width=150)
        self.add_entry_fields["password"] = ckt.CTkEntry(add_frame, placeholder_text="Password", show="*", width=150)
        self.add_entry_fields["notes"] = ckt.CTkEntry(add_frame, placeholder_text="Notes", width=150)

        add_button = ckt.CTkButton(add_frame, text="Add", command=lambda: self.add_pass(type))

        scroll_frame = ckt.CTkScrollableFrame(self.inner_frame, width = 600, height = 700)
        scroll_frame.grid(row=2, column=0, columnspan=3, pady=20, sticky="nsew")

        if type is True:

            self.add_entry_fields["site"].pack(side="left", padx=5, pady=5)
            self.add_entry_fields["username_email"].pack(side="left", padx=5, pady=5)
            self.add_entry_fields["password"].pack(side="left", padx=5, pady=5)
            self.add_entry_fields["notes"].pack(side="left", padx=5, pady=5)
            add_button.pack(side="left", padx=5, pady=5)

            entries = self.dbf.retrieve_passwords(self.uuid)
            for site, username, enc_pass, notes in entries:
                try:
                    decrypted_pass = self.enc.decrypt_data(self.key, enc_pass)
                except Exception as e:
                    print(str(e))
                    decrypted_pass = "<decryption failed>"

                inframe = ckt.CTkFrame(scroll_frame, corner_radius=10)
                inframe.pack(fill="x", pady=5, padx=10)

                label = ckt.CTkLabel(inframe, text=f"{site} \n {username}", anchor="w")
                label.pack(side="left", padx=10, pady=5)

                pass_var = ckt.StringVar(value="••••••••")
                pass_label = ckt.CTkLabel(inframe, textvariable=pass_var, width=150, anchor="w")
                pass_label.pack(side="left", padx=10, pady=5)

                notes_label = ckt.CTkLabel(inframe, text=notes, anchor="w")
                notes_label.pack(side="left", padx=10, pady=5)

                def toggle(var=pass_var, real=decrypted_pass):
                    if var.get() == "••••••••":
                        var.set(real)
                    else:
                        var.set("••••••••")

                show_chk = ckt.CTkCheckBox(inframe, text="Show", command=toggle)
                show_chk.pack(side="right", padx=10)

    def add_pass(self, type):
        if type is True:
            site = self.add_entry_fields["site"].get()
            uname_email = self.add_entry_fields["username_email"].get()
            passw = self.add_entry_fields["password"].get()
            notes = self.add_entry_fields["notes"].get()
            print(self.add_entry_fields)
            print(site, uname_email, passw, notes)

            if not site or not uname_email or not passw:
                mb.showerror("Error", "Site, username/email, and password are required fields.")
                return

            try:
                encpass = self.enc.encrypt_data(self.key, passw)
                print(self.key)
                result, error = self.dbf.add_password(self.uuid, site, uname_email, encpass, notes)
                if result:
                    mb.showinfo("Success", "Password entered successfully")
                    for field in self.add_entry_fields.values():
                        field.delete(0, 'end')
                    self.showPasswords()
                else:
                    mb.showerror("Error", str(error))
                    print()
                    print(error)
            except Exception as e:
                mb.showerror("Error", str(e))
                print()
                print(str(e))

    def showSettings(self):
        self.clear()
        label = ckt.CTkLabel(self.inner_frame, text="Settings", font=config.text_font)
        label.grid(row=0, column=0, sticky="w")

    def clear(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()