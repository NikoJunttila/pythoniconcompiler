import shutil
import os
import tkinter as tk
from tkinter import filedialog, Listbox, Scrollbar, MULTIPLE

def get_svg_files(folder_path, search_term=None):
    svg_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith((".svg", ".png", ".jpg", ".jpeg", ".theme")):
                if search_term is None or search_term.lower() in file.lower():
                    svg_files.append(os.path.join(root, file))
    return svg_files

def copy_files():
    source_folder = source_entry.get()
    destination_folder = destination_entry.get()

    try:
        # Check if the source folder exists
        if not os.path.exists(source_folder):
            result_label.config(text=f"Source folder '{source_folder}' does not exist.")
            return

        # Check if the destination folder exists
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        index_theme_file = os.path.join(source_folder, "index.theme")
        if os.path.isfile(index_theme_file):
            destination_index_theme_file = os.path.join(destination_folder, "index.theme")
            if os.path.isfile(destination_index_theme_file):
                theme_label.config(text="index.theme file already exists in the destination folder.")
            else:
                shutil.copy(index_theme_file, destination_folder)
                theme_label.config(text="index.theme file copied successfully.")
        else:
            theme_label.config(text="No index.theme file found.")


        # Get the selected SVG files
        selected_files = listbox.curselection()
        svg_files = [listbox.get(index) for index in selected_files]

       # Copy the selected SVG files to the destination folder
        for file in svg_files:
            # Get the relative path of the source file
            relative_path = os.path.relpath(file, source_folder)

            # Create the subfolder structure in the destination folder
            destination_subfolder = os.path.dirname(os.path.join(destination_folder, relative_path))
            os.makedirs(destination_subfolder, exist_ok=True)

            # Copy the file to the destination folder
            destination_path = os.path.join(destination_subfolder, os.path.basename(file))
            shutil.copy(file, destination_path)

        result_label.config(text="Files copied successfully.")

    except Exception as e:
        result_label.config(text="An error occurred: " + str(e))

def create_index_theme():
    destination_folder = destination_entry.get()
    index_theme_path = os.path.join(destination_folder, "index.theme")
    name = name_entry.get()
    comment = comment_entry.get()
    inherits = inherits_entry.get()
    try:
        with open(index_theme_path, "w") as f:
            f.write("[Icon Theme]\n")
            f.write(f"Name={name}\n")
            f.write(f"Comment={comment}\n")
            f.write(f"Inherits={inherits}\n")
            f.write("Directories=48x48/apps,48x48@2/apps,48x48/mimetypes,32x32/apps,32x32@2/apps,scalable/apps,scalable/mimetypes\n\n")
            f.write("[scalable/apps]\n")
            f.write("Size=48\n")
            f.write("Type=Scalable\n")
            f.write("MinSize=1\n")
            f.write("MaxSize=256\n")
            f.write("Context=Applications\n\n")
            f.write("[scalable/mimetypes]\n")
            f.write("Size=48\n")
            f.write("Type=Scalable\n")
            f.write("MinSize=1\n")
            f.write("MaxSize=256\n")
            f.write("Context=MimeTypes\n\n")
            f.write("[32x32/apps]\n")
            f.write("Size=32\n")
            f.write("Type=Fixed\n")
            f.write("Context=Applications\n\n")
            f.write("[32x32@2/apps]\n")
            f.write("Size=32\n")
            f.write("Scale=2\n")
            f.write("Type=Fixed\n")
            f.write("Context=Applications\n\n")
            f.write("[48x48/apps]\n")
            f.write("Size=48\n")
            f.write("Type=Fixed\n")
            f.write("Context=Applications\n\n")
            f.write("[48x48@2/apps]\n")
            f.write("Size=48\n")
            f.write("Scale=2\n")
            f.write("Type=Fixed\n")
            f.write("Context=Applications\n\n")
            f.write("[48x48/mimetypes]\n")
            f.write("Size=48\n")
            f.write("Type=Fixed\n")
            f.write("Context=MimeTypes\n")
            theme_label.config(text="index.theme created successfully.")

    except Exception as e:
        theme_label.config(text="An error occurred: " + str(e))


def search_files():
    search_term = search_entry.get()
    source_folder = source_entry.get()

    if not os.path.exists(source_folder):
        result_label.config(text=f"Source folder '{source_folder}' does not exist.")
        return

    svg_files = get_svg_files(source_folder, search_term)
    listbox.delete(0, tk.END)
    for file in svg_files:
        listbox.insert(tk.END, file)

def browse_source_folder():
    folder_path = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, folder_path)
    update_svg_list(folder_path)

def browse_destination_folder():
    folder_path = filedialog.askdirectory()
    destination_entry.delete(0, tk.END)
    destination_entry.insert(0, folder_path)

def update_svg_list(folder_path):
    svg_files = get_svg_files(folder_path)
    listbox.delete(0, tk.END)
    for file in svg_files:
        listbox.insert(tk.END, file)

def update_selected_list():
    selected_files = listbox.curselection()
    selected_listbox.delete(0, tk.END)
    for index in selected_files:
        selected_listbox.insert(tk.END, listbox.get(index))

# Create the GUI window
window = tk.Tk()
window.title("ICON File Copy")
window.geometry("600x350")

# Create labels and entry fields
source_label = tk.Label(window, text="Source Folder:")
source_label.pack()
source_entry = tk.Entry(window, width=40)
source_entry.pack()

destination_label = tk.Label(window, text="Destination Folder:")
destination_label.pack()
destination_entry = tk.Entry(window, width=40)
destination_entry.pack()



# Create buttons
source_button = tk.Button(window, text="Browse source", command=browse_source_folder)
source_button.pack()

destination_button = tk.Button(window, text="Browse destination", command=browse_destination_folder)
destination_button.pack()

# index theme

name_label = tk.Label(window, text="Name:")
name_label.pack()
name_entry = tk.Entry(window, width=30)
name_entry.pack()

comment_label = tk.Label(window, text="Comment:")
comment_label.pack()
comment_entry = tk.Entry(window, width=30)
comment_entry.pack()

inherits_label = tk.Label(window, text="Inherits:")
inherits_label.pack()
inherits_entry = tk.Entry(window, width=30)
inherits_entry.pack()

index_theme = tk.Button(window, text="create theme", command=create_index_theme)
index_theme.pack()


# Create search entry and button
search_label = tk.Label(window, text="Search:")
search_label.pack()
search_entry = tk.Entry(window, width=30)
search_entry.pack()

search_button = tk.Button(window, text="Search", command=search_files)
search_button.pack()

# Create listbox to display SVG files
listbox_frame = tk.Frame(window)
listbox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

listbox_scrollbar = Scrollbar(listbox_frame, orient=tk.VERTICAL)
listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = Listbox(listbox_frame, selectmode=MULTIPLE)
listbox.pack(fill=tk.BOTH, expand=True)
listbox.config(yscrollcommand=listbox_scrollbar.set)
listbox_scrollbar.config(command=listbox.yview)

# Create listbox to display selected SVG files
selected_frame = tk.Frame(window)
selected_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

selected_listbox_scrollbar = Scrollbar(selected_frame, orient=tk.VERTICAL)
selected_listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

selected_listbox = Listbox(selected_frame)
selected_listbox.pack(fill=tk.BOTH, expand=True)
selected_listbox.config(yscrollcommand=selected_listbox_scrollbar.set)
selected_listbox_scrollbar.config(command=selected_listbox.yview)

# Create button to copy files
copy_button = tk.Button(window, text="Copy Files", command=copy_files)
copy_button.pack()

# Create result label
result_label = tk.Label(window, text="")
result_label.pack()
theme_label = tk.Label(window, text="")
theme_label.pack()

# Bind selection event to update selected listbox
listbox.bind("<<ListboxSelect>>", lambda event: update_selected_list())

# Run the GUI
window.mainloop()