from ctypes import POINTER, pointer, sizeof, windll, Structure, byref, c_int
from ctypes.wintypes import DWORD, ULONG

class AccentPolicy(Structure):
    _fields_ = [
        ('AccentState',   DWORD),
        ('AccentFlags',   DWORD),
        ('GradientColor', DWORD),
        ('AnimationId',   DWORD), ]

class WindowCompositionAttributes(Structure):
    _fields_ = [
        ('Attribute',  DWORD),
        ('Data',       POINTER(AccentPolicy)),
        ('SizeOfData', ULONG),]


class ChangeHeaderColor:
    """ change the titlebar background color """

    def __init__(self,
                 window,
                 color):

        self.HWND = detect(window)

        if color == "transparent":
            ChangeDWMAccent(self.HWND, 30, 2)
            return
        else:
            ChangeDWMAccent(self.HWND, 30, 0)

        self.color = DWORD(int(convert_color(color), base=16))
        self.attrib = 35
        ChangeDWMAttrib(self.HWND, self.attrib, self.color)


class ChangeBorderColor:
    """ change the window border color """

    def __init__(self, window, color):
        self.HWND = detect(window)
        self.color = DWORD(int(convert_color(color), base=16))
        self.attrib = 34
        ChangeDWMAttrib(self.HWND, self.attrib, self.color)


class ChangeTitleColor:
    """ change the title color """

    def __init__(self, window, color):
        self.HWND = detect(window)
        self.color = DWORD(int(convert_color(color), base=16))
        self.attrib = 36
        ChangeDWMAttrib(self.HWND, self.attrib, self.color)


class ApplyStyle:
    """ different styles for windows """

    def __init__(self, window):
        self.HWND = detect(window)
        window.config(bg="black")
        ChangeDWMAccent(self.HWND, 30, 2)
        ChangeDWMAccent(self.HWND, 19, 4, color=0x292929)


def ChangeDWMAccent(hwnd: int, attrib: int, state: int, color=None):
    accent_policy = AccentPolicy()

    win_comp_attr_data = WindowCompositionAttributes()
    win_comp_attr_data.Attribute = attrib
    win_comp_attr_data.SizeOfData = sizeof(accent_policy)
    win_comp_attr_data.Data = pointer(accent_policy)

    accent_policy.AccentState = state
    if color:
        accent_policy.GradientColor = color

    windll.user32.SetWindowCompositionAttribute(hwnd, pointer(win_comp_attr_data))

def ChangeDWMAttrib(h_wnd: int, attrib: int, color):
    windll.dwmapi.DwmSetWindowAttribute(h_wnd, attrib, byref(color), sizeof(c_int))

def detect(window):
    window.update()
    return windll.user32.GetParent(window.winfo_id())


def convert_color(color_name: str):
    """ convert colors to the required API """
    names_to_hex = {
        "aliceblue": "#f0f8ff",
        "antiquewhite": "#faebd7",
        "aqua": "#00ffff",
        "aquamarine": "#7fffd4",
        "azure": "#f0ffff",
        "beige": "#f5f5dc",
        "bisque": "#ffe4c4",
        "black": "#000000",
        "blanchedalmond": "#ffebcd",
        "blue": "#0000ff",
        "blueviolet": "#8a2be2",
        "brown": "#a52a2a",
        "burlywood": "#deb887",
        "cadetblue": "#5f9ea0",
        "chartreuse": "#7fff00",
        "chocolate": "#d2691e",
        "coral": "#ff7f50",
        "cornflowerblue": "#6495ed",
        "cornsilk": "#fff8dc",
        "crimson": "#dc143c",
        "cyan": "#00ffff",
        "darkblue": "#00008b",
        "darkcyan": "#008b8b",
        "darkgoldenrod": "#b8860b",
        "darkgray": "#a9a9a9",
        "darkgrey": "#a9a9a9",
        "darkgreen": "#006400",
        "darkkhaki": "#bdb76b",
        "darkmagenta": "#8b008b",
        "darkolivegreen": "#556b2f",
        "darkorange": "#ff8c00",
        "darkorchid": "#9932cc",
        "darkred": "#8b0000",
        "darksalmon": "#e9967a",
        "darkseagreen": "#8fbc8f",
        "darkslateblue": "#483d8b",
        "darkslategray": "#2f4f4f",
        "darkslategrey": "#2f4f4f",
        "darkturquoise": "#00ced1",
        "darkviolet": "#9400d3",
        "deeppink": "#ff1493",
        "deepskyblue": "#00bfff",
        "dimgray": "#696969",
        "dimgrey": "#696969",
        "dodgerblue": "#1e90ff",
        "firebrick": "#b22222",
        "floralwhite": "#fffaf0",
        "forestgreen": "#228b22",
        "fuchsia": "#ff00ff",
        "gainsboro": "#dcdcdc",
        "ghostwhite": "#f8f8ff",
        "gold": "#ffd700",
        "goldenrod": "#daa520",
        "gray": "#808080",
        "grey": "#808080",
        "green": "#008000",
        "greenyellow": "#adff2f",
        "honeydew": "#f0fff0",
        "hotpink": "#ff69b4",
        "indianred": "#cd5c5c",
        "indigo": "#4b0082",
        "ivory": "#fffff0",
        "khaki": "#f0e68c",
        "lavender": "#e6e6fa",
        "lavenderblush": "#fff0f5",
        "lawngreen": "#7cfc00",
        "lemonchiffon": "#fffacd",
        "lightblue": "#add8e6",
        "lightcoral": "#f08080",
        "lightcyan": "#e0ffff",
        "lightgoldenrodyellow": "#fafad2",
        "lightgray": "#d3d3d3",
        "lightgrey": "#d3d3d3",
        "lightgreen": "#90ee90",
        "lightpink": "#ffb6c1",
        "lightsalmon": "#ffa07a",
        "lightseagreen": "#20b2aa",
        "lightskyblue": "#87cefa",
        "lightslategray": "#778899",
        "lightslategrey": "#778899",
        "lightsteelblue": "#b0c4de",
        "lightyellow": "#ffffe0",
        "lime": "#00ff00",
        "limegreen": "#32cd32",
        "linen": "#faf0e6",
        "magenta": "#ff00ff",
        "maroon": "#800000",
        "mediumaquamarine": "#66cdaa",
        "mediumblue": "#0000cd",
        "mediumorchid": "#ba55d3",
        "mediumpurple": "#9370db",
        "mediumseagreen": "#3cb371",
        "mediumslateblue": "#7b68ee",
        "mediumspringgreen": "#00fa9a",
        "mediumturquoise": "#48d1cc",
        "mediumvioletred": "#c71585",
        "midnightblue": "#191970",
        "mintcream": "#f5fffa",
        "mistyrose": "#ffe4e1",
        "moccasin": "#ffe4b5",
        "navajowhite": "#ffdead",
        "navy": "#000080",
        "oldlace": "#fdf5e6",
        "olive": "#808000",
        "olivedrab": "#6b8e23",
        "orange": "#ffa500",
        "orangered": "#ff4500",
        "orchid": "#da70d6",
        "palegoldenrod": "#eee8aa",
        "palegreen": "#98fb98",
        "paleturquoise": "#afeeee",
        "palevioletred": "#db7093",
        "papayawhip": "#ffefd5",
        "peachpuff": "#ffdab9",
        "peru": "#cd853f",
        "pink": "#ffc0cb",
        "plum": "#dda0dd",
        "powderblue": "#b0e0e6",
        "purple": "#800080",
        "red": "#ff0000",
        "rosybrown": "#bc8f8f",
        "royalblue": "#4169e1",
        "saddlebrown": "#8b4513",
        "salmon": "#fa8072",
        "sandybrown": "#f4a460",
        "seagreen": "#2e8b57",
        "seashell": "#fff5ee",
        "sienna": "#a0522d",
        "silver": "#c0c0c0",
        "skyblue": "#87ceeb",
        "slateblue": "#6a5acd",
        "slategray": "#708090",
        "slategrey": "#708090",
        "snow": "#fffafa",
        "springgreen": "#00ff7f",
        "steelblue": "#4682b4",
        "tan": "#d2b48c",
        "teal": "#008080",
        "thistle": "#d8bfd8",
        "tomato": "#ff6347",
        "turquoise": "#40e0d0",
        "violet": "#ee82ee",
        "wheat": "#f5deb3",
        "white": "#ffffff",
        "whitesmoke": "#f5f5f5",
        "yellow": "#ffff00",
        "yellowgreen": "#9acd32",
    }

    if not color_name.startswith("#"):
        if color_name in names_to_hex:
            color = names_to_hex[color_name]
        elif color_name.startswith("grey") or color_name.startswith("gray"):
            color = f"#{color_name[-2:]}{color_name[-2:]}{color_name[-2:]}"
        else:
            raise ValueError(f"Invalid color passed: {color_name}")
    else:
        color = color_name

    color = f"{color[5:7]}{color[3:5]}{color[1:3]}"
    return color

