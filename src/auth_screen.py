import customtkinter as ckt
from tkinter import messagebox as mb
from . import config
from . import db
from . import encryption_logic

class AuthScreen(ckt.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.center_frame = ckt.CTkFrame(self, fg_color="transparent")
        self.center_frame.pack(expand=True)

        self.login_view()
        self.dbf = db.DBfunc()
        self.enc = encryption_logic.EncryptionHandler()

    def clear(self):
        for widget in self.center_frame.winfo_children():
            widget.destroy()

    def login(self):
        inputuser, inputpass = self.username_entry.get(), self.password_entry.get()
        dbuserdata = self.dbf.retrieve_account(inputuser)

        if dbuserdata is None:
            mb.showerror("Error", "Input username or password is wrong or does not exist!")
            return
        try:
            dbpass = dbuserdata[1]
            if self.enc.verify_password(inputpass, dbpass):
                mb.showinfo("Success", "Successfully logged in")
                self.master.show_main_app()
                self.master.uuid = dbuserdata[0]
            else:
                mb.showerror("Error", "Something went wrong")
        except Exception as e:
                mb.showerror("Error", e)

    def register_user(self):
        inputuser, inputpass = self.username_entry.get(), self.password_entry.get()
        dbuserdata = self.dbf.retrieve_account(inputuser)

        if dbuserdata is not None:
            mb.showerror("Error", "Input username already exist!")
            return

        try:
            hashpass = self.enc.hash_password(inputpass)
            salt = self.enc.gen_salt()
            uuid = self.enc.gen_uuid(inputuser, hashpass, salt)
            result, error = self.dbf.enter_account(uuid, inputuser, hashpass, salt)
            if result and not error:
                mb.showinfo("Succes", "User successfully registered\n Please Log in.")
                self.login_view()
            else:
                mb.showerror("Error", error)
        except Exception as e:
            mb.showerror("Error", str(e))

    def login_view(self):
        self.clear()

        label = ckt.CTkLabel(self.center_frame, text="Login", font=("Roboto", 24, "bold"))
        label.pack(pady=(0, 20))

        self.username_entry = ckt.CTkEntry(self.center_frame, placeholder_text="Username", width=300, font=config.search_font)
        self.username_entry.pack(pady=(0, 10))

        self.password_entry = ckt.CTkEntry(self.center_frame, placeholder_text="Password", show="*", width=300, font=config.search_font)
        self.password_entry.pack(pady=(0, 20))

        login_button = ckt.CTkButton(self.center_frame, text="Login", width=300, command=self.login)
        login_button.pack()

        register_switch_button = ckt.CTkButton(self.center_frame, text="Don't have an account? Register", fg_color="transparent", hover=False, command=self.register_view)
        register_switch_button.pack(pady=(10, 0))

    def register_view(self):
        self.clear()

        label = ckt.CTkLabel(self.center_frame, text="Register", font=("Roboto", 24, "bold"))
        label.pack(pady=(0, 20))

        self.username_entry = ckt.CTkEntry(self.center_frame, placeholder_text="Choose a username", width=300, font=config.search_font)
        self.username_entry.pack(pady=(0, 10))

        self.password_entry = ckt.CTkEntry(self.center_frame, placeholder_text="Enter a strong password", show="*", width=300, font=config.search_font)
        self.password_entry.pack(pady=(0, 10))

        register_button = ckt.CTkButton(self.center_frame, text="Register", width=300, command=self.register_user)
        register_button.pack()

        login_switch_button = ckt.CTkButton(self.center_frame, text="Already have an account? Login", fg_color="transparent", hover=False, command=self.login_view)
        login_switch_button.pack(pady=(10, 0))