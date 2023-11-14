from tkinter import Widget

def getFullName(widget: Widget):
    name_list = [widget.winfo_name()]
    while True:
        widget = widget.master
        name = widget.winfo_name()
        if name == "tk":
            name_list.append("")
            return ".".join(reversed(name_list))
        name_list.append(name)