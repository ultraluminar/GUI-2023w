def center_window(window, width: int, height: int):
    pos_x = round((window.winfo_screenwidth() / 2) - (width / 2))
    pos_y = round((window.winfo_screenheight() / 2) - (height / 2))

    window.geometry(f"{width}x{height}+{pos_x}+{pos_y}")