import HarvestTaskAdderUI as htau
import HarvestTaskAdderScript as htas
from tkinter import messagebox


def on_close():
    try:
        if len(htas.module_prefix) > 0:
            clear_before_close = messagebox.askyesno("Clear Tasks",
                                                     "Would you like to clear your current tasks before you go?")
        else:
            root.root.destroy()
        if clear_before_close is True:
            root.clear_module_prefixes()
            htau.save_data()
            root.root.destroy()
        else:
            root.root.destroy()
    except:
        return


root = htau.Main_Window()
try:
    htau.start_up()
except:
    pass

root.main_widgets()
root.root.protocol("WM_DELETE_WINDOW", on_close)
root.root.mainloop()



