import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import PIL
DEFAULT_IMAGE_PATH = "DefaultPics/shapes.png"  # Replace with the path to your default photo

def browse_file():
    file_path = filedialog.askopenfilename()
    print("Selected File:", file_path)

def resize_image(image, size):
    # Resize the image to a square shape
    thumb = image.copy()
    thumb.thumbnail(size, PIL.Image.LANCZOS )
    offset = (max((size[0] - thumb.size[0]) // 2, 0), max((size[1] - thumb.size[1]) // 2, 0))
    square_image = Image.new('RGB', size, (255, 255, 255))
    square_image.paste(thumb, offset)
    return square_image

def add_row():
    frame = tk.Frame(listbox)
    frame.pack(side=tk.TOP, fill=tk.X)

    # Browse Image Widgets
    image_preview = tk.Label(frame)
    image_preview.pack(side=tk.LEFT)

    def update_image_preview():
        image_path = filedialog.askopenfilename()
        if image_path:
            image = Image.open(image_path)
            # Resize the image to a square shape
            image = resize_image(image, (100, 100))
            photo = ImageTk.PhotoImage(image)
            image_preview.config(image=photo)
            image_preview.image = photo  # Keep a reference to prevent garbage collection of the image

    image_button = tk.Button(frame, text="Browse Image", command=update_image_preview)
    image_button.pack(side=tk.LEFT)

    # File Address Display
    file_address = tk.Entry(frame)
    file_address.pack(side=tk.LEFT)

    browse_button = tk.Button(frame, text="Browse", command=browse_file)
    browse_button.pack(side=tk.LEFT)

    # Set default image
    default_image = Image.open(DEFAULT_IMAGE_PATH)
    # Resize the default image to a square shape
    default_image = resize_image(default_image, (100, 100))
    default_photo = ImageTk.PhotoImage(default_image)
    image_preview.config(image=default_photo)
    image_preview.image = default_photo

def remove_row():
    if listbox.size() > 0:
        listbox.delete(tk.END)

root = tk.Tk()
root.title("Scroll Bar Example")

# Create a Scrollbar
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a Listbox to hold the scrollable items
listbox = tk.Listbox(root, yscrollcommand=scrollbar.set)
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

# Configure the Scrollbar to scroll the Listbox
scrollbar.config(command=listbox.yview)

# Add initial rows to the Listbox
add_row()
add_row()

# Add Button Widgets
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM)

add_button = tk.Button(button_frame, text="Add", command=add_row)
add_button.pack(side=tk.LEFT)

remove_button = tk.Button(button_frame, text="Remove", command=remove_row)
remove_button.pack(side=tk.LEFT)

root.mainloop()