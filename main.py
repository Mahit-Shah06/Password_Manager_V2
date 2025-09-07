from src.gui import GUI
from src.db import DBfunc

if __name__ == "__main__":

    DBfunc.initialize_tables
    app = GUI()
    app.mainloop()