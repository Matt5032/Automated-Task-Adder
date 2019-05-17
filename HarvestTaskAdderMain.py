from HarvestTaskAdderUI import *
from HarvestTaskAdderScript import *
import pickle




def on_close():
    try:
        if len(module_prefix) > 0:
           clear_before_close = messagebox.askyesno("Clear Tasks", "Would you like to clear your current tasks before you go?")
        else:
            root.root.destroy()
        if clear_before_close == True:
            root.clear_module_prefixes()
            save_data()
            root.root.destroy()
        else:
            root.root.destroy()
    except:
        return





root = Main_Window()
try:
    start_up()
except:
    pass
root.main_widgets()
root.root.protocol("WM_DELETE_WINDOW", on_close)
root.root.mainloop()



