# ui_app.py

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from opencv import find_all_shapes

class ShapeDetectionApp:
    def __init__(self, master):
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

        self.template_listbox = tk.Listbox(self.master, selectmode=tk.SINGLE, height=5, width=50)
        self.template_listbox.grid(row=2, column=1, padx=5, pady=5, rowspan=2)

        tk.Button(self.master, text="Add Template", command=self.add_template).grid(row=4, column=1, padx=5, pady=5, sticky='e')
        tk.Button(self.master, text="Remove Template", command=self.remove_template).grid(row=4, column=1, padx=(0, 130), pady=5, sticky='e')

        # Checkbox for using pre-saved templates
        self.pre_saved_var = tk.BooleanVar()
        self.pre_saved_var.set(True)
        tk.Checkbutton(self.master, text="Use pre-saved templates", variable=self.pre_saved_var).grid(row=6, column=1, padx=5, pady=5)

        # Run Detection button
        tk.Button(self.master, text="Run Detection", command=self.run_detection).grid(row=7, column=1, pady=10)

        # Variable to store the selected output folder
        self.output_folder_var = tk.StringVar()

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

    def add_template(self):
        file_path = filedialog.askopenfilename(title="Select a Template Image", filetypes=[("Image files", "*.*")])
        if file_path and file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            self.template_listbox.insert(tk.END, file_path)

    def remove_template(self):
        selected_index = self.template_listbox.curselection()
        if selected_index:
            self.template_listbox.delete(selected_index)

if __name__ == "__main__":
    root = tk.Tk()
    app = ShapeDetectionApp(root)
    root.mainloop()
