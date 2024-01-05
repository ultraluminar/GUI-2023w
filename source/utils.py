def center_window(window, width: int, height: int):
    """
    Centers the given window on the screen based on the specified width and height.

    Args:
        window: The window to be centered.
        width (int): The width of the window.
        height (int): The height of the window.
    """
    pos_x = round((window.winfo_screenwidth() / 2) - (width / 2))
    pos_y = round((window.winfo_screenheight() / 2) - (height / 2))

    window.geometry(f"{width}x{height}+{pos_x}+{pos_y}")