import math

def get_color_name(r, g, b, a=255):
    if a < 5:
        return "Transparent"

    colors = {
        (0, 0, 0): "Black", (255, 255, 255): "White", (255, 0, 0): "Red",
        (0, 255, 0): "Lime", (0, 0, 255): "Blue", (255, 255, 0): "Yellow",
        (0, 255, 255): "Cyan", (255, 0, 255): "Magenta", (192, 192, 192): "Silver",
        (128, 128, 128): "Gray", (128, 0, 0): "Maroon", (128, 128, 0): "Olive",
        (0, 128, 0): "Green", (128, 0, 128): "Purple", (0, 128, 128): "Teal",
        (0, 0, 128): "Navy", (255, 165, 0): "Orange", (255, 20, 147): "Deep Pink",
        (30, 30, 30): "Dark Grey",
    }
    min_dist = float("inf"); closest_name = "Custom Color"
    for (cr, cg, cb), name in colors.items():
        dist = math.sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)
        if dist < min_dist: min_dist = dist; closest_name = name
    if min_dist < 60:
        return f"Transparent {closest_name}" if a < 200 else closest_name
    return "Custom Color"