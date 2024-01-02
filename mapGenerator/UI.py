import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, simpledialog
from opencv import find_all_shapes
from PIL import Image, ImageTk
import uuid
import PIL

DEFAULT_IMAGE_PATH = "DefaultPics/Default.png"

class ShapeDetectionApp:
    def __init__(self, master):
        self.template_frames = []
        self.image_tuples = []
        self.master = master
        self.master.title("Shape Detection")

        # Widgets for source image selection
        tk.Label(self.master, text="Source Image:").grid(row=0, column=0, padx=5, pady=5)
        self.source_entry = tk.Entry(self.master, width=50)
        self.source_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.master, text="Open", command=self.open_file).grid(row=0, column=2, padx=5, pady=5)

        # Widgets for output folder selection
        tk.Label(self.master, text="Output Image:").grid(row=1, column=0, padx=5, pady=5)
        self.output_entry = tk.Entry(self.master, width=50)
        self.output_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.master, text="Select Folder", command=self.select_output_folder).grid(row=1, column=2, padx=5, pady=5)

        # Widgets for user templates
        tk.Label(self.master, text="User Templates:").grid(row=2, column=0, padx=5, pady=5)

        max_canvas_height = 10  # Set your desired maximum height
        canvas_width = 50  # Set your desired width

        self.margin_frame = tk.Frame(self.master, padx=20, pady=20, bg="black")
        self.margin_frame.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        self.canvas = tk.Canvas(self.master, height=200 , width= 460, bg=self.source_entry.cget("bg")) 
        self.canvas.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        self.scrollbar = tk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=2, column=2, padx=5, pady=5, sticky='ns')

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Frame to hold the template widgets
        self.template_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.template_frame, anchor="nw", width=460, background=self.on_frame_configure(self.canvas))

        # Add a bind to the canvas to update scroll region when the frame size changes
        self.template_frame.bind("<Configure>", lambda event, canvas=self.canvas: self.on_frame_configure(canvas))

        tk.Button(self.master, text="Add Template", command=self.add_template).grid(row=4, column=1, padx=5, pady=5, sticky='e')
        tk.Button(self.master, text="Remove Template", command=self.remove_template).grid(row=4, column=1, padx=(0, 130), pady=5, sticky='e')

        separator = ttk.Separator(self.master, orient="horizontal")
        separator.grid(row=6, column=0, columnspan=3, sticky="ew", pady=10)
        # Run Detection button
        tk.Button(self.master, text="Run Detection", command=self.run_detection).grid(row=7, column=2, padx=(0, 10), pady=(0,10), sticky='w')
        tk.Button(self.master, text="cancel").grid(row=7, column=1, padx=10, pady=(0,10), sticky='e')

        # Variable to store the selected output folder
        self.output_folder_var = tk.StringVar()

    def on_frame_configure(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def open_file(self):
        file_path = filedialog.askopenfilename(title="Select a Source Image", filetypes=[("Image files", "*.*")])
        if file_path and file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, file_path)

    def select_output_folder(self):
        folder_path = filedialog.askdirectory(title="Select Output Folder")
        if folder_path:
            self.output_folder_var.set(folder_path)
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder_path)

    def run_detection(self):
        source_image_path = self.source_entry.get()
        output_folder_path = self.output_folder_var.get()

        if source_image_path and output_folder_path:
            use_pre_saved_templates = self.pre_saved_var.get()

            if use_pre_saved_templates:
                # Use pre-saved templates
                template_paths = [
                    "path/to/template/unknown_shape_1.jpg",
                    "path/to/template/unknown_shape_2.jpg",
                    # Add more template paths as needed
                ]
            else:
                # Use user-provided templates
                template_paths = [self.template_listbox.get(idx) for idx in range(self.template_listbox.size())]

            find_all_shapes(source_image_path, template_paths, os.path.join(output_folder_path, "result_image.jpg"))
            messagebox.showinfo("Complete", "Shape detection completed!")

    def resize_image(self, image, size):
        # Resize the image to a square shape
        thumb = image.copy()
        thumb.thumbnail(size, PIL.Image.LANCZOS)
        square_image = Image.new('RGBA', size, (0, 0, 0, 0))
        offset = (max((size[0] - thumb.size[0]) // 2, 0), max((size[1] - thumb.size[1]) // 2, 0))
        square_image.paste(thumb, offset)
        return square_image

    def find_tuple_by_second_item(self, list_of_tuples, target_value):
        for tpl in list_of_tuples:
            if len(tpl) > 1 and tpl[1] == target_value:
                return tpl[0]
        return None

    def add_template(self):
        frame_id = str(uuid.uuid4())
        frame = tk.Frame(self.template_frame, relief=tk.SOLID, highlightthickness=2, highlightbackground = self.source_entry.cget("bg"))
        frame.pack(side=tk.TOP, fill=tk.X, )

        frame.id = frame_id
        # Browse Image Widgets
        image_preview = tk.Label(frame)
        image_preview.pack(side=tk.LEFT)

        image_preview_2 = tk.Label(frame)
        image_preview_2.pack(side=tk.RIGHT)

        def update_image_preview():
            image_path = filedialog.askopenfilename()
            if image_path:
                image_tuple = (image_path,)  # Create a tuple with the first image path
                self.image_tuples.append((image_tuple,frame.id))
                image = Image.open(image_path)
                # Resize the image to a square shape
                image = self.resize_image(image, (50, 50))
                photo = ImageTk.PhotoImage(image)
                image_preview.config(image=photo)
                image_preview.image = photo  # Keep a reference to prevent garbage collection of the image

        def update_image_preview_2():
            selected_option = selected_option_var.get()
            if selected_option == "Browse Image":
                image_path = filedialog.askopenfilename()
            elif selected_option == "Presaved":
                specific_folder_path = "3D shapes"  # Set the specific folder path
                image_path = filedialog.askopenfilename(initialdir=specific_folder_path)
                
            
            if image_path:
                 # Check if there's a tuple for the current frame
                if self.image_tuples and self.find_tuple_by_second_item(self.image_tuples, frame.id) != None:
                    # If a tuple with one image path exists, add the second image path to the tuple
                    for index, my_tuple in enumerate(self.image_tuples):
                        if my_tuple[1] == frame.id:
                        # Create a new tuple with the same first item and the updated second item
                            updated_tuple = ((my_tuple[0], image_path), frame.id)
                         # Replace the old tuple with the updated one in the list
                            self.image_tuples[index] = updated_tuple 
                else:
                    # Create a new tuple with the second image path
                    image_tuple = ('',image_path)
                    self.image_tuples.append((image_tuple,frame.id))
                image = Image.open(image_path)
                # Resize the image to a square shape
                image = self.resize_image(image, (50, 50))
                photo = ImageTk.PhotoImage(image)
                image_preview_2.config(image=photo)
                image_preview_2.image = photo

        image_button = tk.Button(frame, text="Browse Image", command=update_image_preview)
        image_button.pack(side=tk.LEFT)

        options = ["Browse Image", "Presaved"]

        selected_option_var = tk.StringVar()
        selected_option_var.set(options[0])  # Set the initial value

        dropdown_menu = tk.OptionMenu(frame, selected_option_var, *options)
        dropdown_menu.pack(side=tk.RIGHT)

        def dropdown_callback(*args):
            update_image_preview_2()

        # Bind the callback to the dropdown menu
        selected_option_var.trace_add("write", dropdown_callback)

        # Set default image
        default_image = Image.open(DEFAULT_IMAGE_PATH)
        # Resize the default image to a square shape
        default_image = self.resize_image(default_image, (50, 50))
        default_photo = ImageTk.PhotoImage(default_image)
        image_preview.config(image=default_photo)
        image_preview.image = default_photo
        image_preview_2.config(image=default_photo)
        image_preview_2.image = default_photo

        self.template_frames.append(frame)

    def remove_template(self):
        if self.template_frames:
        # Get the last frame in the list
            last_template = self.template_frames[-1]

            # Destroy the last frame
            last_template.destroy()

            # Remove the last frame from the list
            self.template_frames.pop()
            if self.find_tuple_by_second_item(self.image_tuples, last_template.id) != None:
                self.image_tuples.remove((self.find_tuple_by_second_item(self.image_tuples, last_template.id), last_template.id))
            # Reset the selected template
            self.selected_template = None


if __name__ == "__main__":
    root = tk.Tk()
    app = ShapeDetectionApp(root)
    root.mainloop()
