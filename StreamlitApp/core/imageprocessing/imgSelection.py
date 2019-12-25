from skimage import data

def process_selection(img_selected):
    if img_selected == "ASTRONAUT":
        return data.astronaut()
    if img_selected == "CHECKER":
        return data.checkerboard()
    if img_selected == "COINS":
        return data.coins()
    if img_selected == "HUBBLE":
        return data.hubble_deep_field()
    if img_selected == "HORSE":
        return data.horse()
    if img_selected == "CAMERA":
        return data.camera()
    if img_selected == "COFFEE":
        return data.coffee()
    else:
        return data.astronaut()

