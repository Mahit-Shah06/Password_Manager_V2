from src.gui import GUI
from src.db import DBfunc

if __name__ == "__main__":

    db = DBfunc()
    db.initialize_tables()
    app = GUI()
    app.mainloop()