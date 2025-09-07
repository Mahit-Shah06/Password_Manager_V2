from src.gui import GUI
from src.db import DBfunc
import os

if __name__ == "__main__":

    db = DBfunc()
    db.initialize_tables()
    print("DB connected")
    print("DB absolute path:", os.path.abspath("pswmgrv2.db"))
    app = GUI()
    app.mainloop()
    print("GUI Initialized")