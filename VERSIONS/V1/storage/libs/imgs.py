from PIL import Image, ImageTk, ImageFilter

def change_opacity(image, opacity):
    transparent_image = Image.new('RGB', image.size, (0, 0, 0))
    return Image.blend(image, transparent_image, opacity)