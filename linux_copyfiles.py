import shutil
import os
import tkinter as tk
from tkinter import filedialog, Listbox, Scrollbar, MULTIPLE, Label, PhotoImage, Scrollbar, Button, Entry
from PIL import Image, ImageTk
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
import glob
import subprocess


def get_svg_files(folder_path, search_term=None):
    svg_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith((".svg", ".png", ".jpg", ".jpeg")):
                if search_term is None or search_term.lower() in file.lower():
                    svg_files.append(os.path.join(root, file))
    return svg_files

def get_themes(folder_path, search_term=None):
    themes = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".theme"):
                if search_term is None or search_term.lower() in file.lower():
                    themes.append(os.path.join(root, file))
    return themes


selected_files2 = []
full_path_arr = []
 
def push_item():
    item = entry.get()
    if item:
        names_to_match.append(item)
        update_array()

def update_array():
    array_label['text'] = ", ".join(names_to_match)

names_to_match = [] 

#copy files from arrray in code
def copyfiles():
    source_folder = source_entry.get()
    destination_folder = destination_entry.get()
    svg_files = get_svg_files(source_folder) 
    index_themes = get_themes(source_folder)  

    try:
        # Check if the source folder exists
        if not os.path.exists(source_folder):
            return

        # Check if the destination folder exists
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        for file in index_themes:
            file_name = os.path.basename(file)
            relative_path = os.path.relpath(file, source_folder)

            destination_subfolder = os.path.dirname(os.path.join(destination_folder, relative_path))
            os.makedirs(destination_subfolder, exist_ok=True)

            destination_path = os.path.join(destination_subfolder, os.path.basename(file))

    # Check if the destination folder already contains the index.theme file
            if not os.path.exists(destination_path):
                shutil.copy(file, destination_path)
        
       # index_theme_file = os.path.join(source_folder, "index.theme")
       # if os.path.isfile(index_theme_file):
        #    destination_index_theme_file = os.path.join(destination_folder, "index.theme")
        #    if os.path.isfile(destination_index_theme_file):
        #        print("theme found")
        #    else:
        #        shutil.copy(index_theme_file, destination_folder)
        #else:
        #    print("not found index.theme")


        for file in svg_files:
            file_name = os.path.basename(file)
            split_name = file_name.split(".")[0]
            if split_name in names_to_match:
            # Get the relative path of the source file
                relative_path = os.path.relpath(file, source_folder)

            # Create the subfolder structure in the destination folder
                destination_subfolder = os.path.dirname(os.path.join(destination_folder, relative_path))
                os.makedirs(destination_subfolder, exist_ok=True)

            # Copy the file to the destination folder
                destination_path = os.path.join(destination_subfolder, os.path.basename(file))
                shutil.copy(file, destination_path)
        update_added_icons_list(destination_folder)

    except Exception as e:
        result_label.config(text="An error occurred: " + str(e))


def copy_files():
    source_folder = source_entry.get()
    destination_folder = destination_entry.get()
    index_themes = get_themes(source_folder)
    global selected_files2
    try:
        # Check if the source folder exists
        if not os.path.exists(source_folder):
            result_label.config(text=f"Source folder '{source_folder}' does not exist.")
            return

        # Check if the destination folder exists
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        for file in index_themes:	
            file_name = os.path.basename(file)	
            relative_path = os.path.relpath(file, source_folder)	
            destination_subfolder = os.path.dirname(os.path.join(destination_folder, relative_path))	
            os.makedirs(destination_subfolder, exist_ok=True)	
            destination_path = os.path.join(destination_subfolder, os.path.basename(file))	
    # Check if the destination folder already contains the index.theme file	
            if not os.path.exists(destination_path):	
                theme_label.config(text="index.theme copied successfully.")	
                shutil.copy(file, destination_path)

        selected_files = listbox.curselection()
        for x in selected_files:
            selected_files2.append(full_path_arr[x])


       # Copy the selected SVG files to the destination folder
        for file in selected_files2:
            # Get the relative path of the source file
            relative_path = os.path.relpath(file, source_folder)

            # Create the subfolder structure in the destination folder
            destination_subfolder = os.path.dirname(os.path.join(destination_folder, relative_path))
            os.makedirs(destination_subfolder, exist_ok=True)

            # Copy the file to the destination folder
            destination_path2 = os.path.join(destination_subfolder, os.path.basename(file))	
            if os.path.exists(destination_path2):	
                print(f"File '{os.path.basename(file)}' already exists in the destination folder.")	
            else:	
                shutil.copy(file, destination_path2)

        result_label.config(text="Files copied successfully.")
        update_added_icons_list(destination_folder)
        listbox.selection_clear(0, tk.END)
        selected_listbox.delete(0, tk.END)  # Empty the selected listbox
        selected_files2.clear()

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
    global selected_files2
    search_term = search_entry.get()
    source_folder = source_entry.get()

    selected_files = listbox.curselection()
    for x in selected_files:
        selected_files2.append(full_path_arr[x])

    if not os.path.exists(source_folder):
        result_label.config(text=f"Source folder '{source_folder}' does not exist.")
        return

    full_path_arr.clear()
    svg_files = get_svg_files(source_folder, search_term)
    listbox.delete(0, tk.END)
    for file in svg_files:
        file_name = os.path.basename(file)
        folder_name = os.path.basename(os.path.dirname(file))
        full = folder_name + "/" + file_name
        listbox.insert(tk.END, full)
        full_path_arr.append(file)

def browse_source_folder():
    folder_path = ask_directory_with_create_new_folder()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, folder_path)
    update_svg_list(folder_path)

def browse_destination_folder():
    folder_path = ask_directory_with_create_new_folder()
    destination_entry.delete(0, tk.END)
    destination_entry.insert(0, folder_path)
    update_added_icons_list(folder_path)

def browse_source_code_folder():
    folder_path = ask_directory_with_create_new_folder()
    source_code_entry.delete(0, tk.END)
    source_code_entry.insert(0, folder_path)
    find_icons_in_files(folder_path)
    update_array()

def update_svg_list(folder_path):
    svg_files = get_svg_files(folder_path)
    listbox.delete(0, tk.END)
    for file in svg_files:
        file_name = os.path.basename(file)
        folder_name = os.path.basename(os.path.dirname(file))
        full = folder_name + "/" + file_name
        listbox.insert(tk.END, full)
        full_path_arr.append(file)

def update_selected_list():
    selected_files = listbox.curselection()
    global selected_files2

    selected_listbox.delete(0, tk.END)
    for x in selected_files:
        selected_listbox.insert(tk.END, full_path_arr[x])
    if selected_files2:
        for item in selected_files2:
           selected_listbox.insert(tk.END, item)
    show_image()

added_icons_arr = []
def update_added_icons_list(folder_path):
    added_icons_listbox.delete(0, tk.END)
    added_icons = get_svg_files(folder_path)
    added_icons_arr.clear()
    for icon in added_icons:
        file_name = os.path.basename(icon)
        folder_name = os.path.basename(os.path.dirname(icon))
        full = folder_name + "/" + file_name
        added_icons_arr.append(icon)
        added_icons_listbox.insert(tk.END, full)

def change_resolution(image_path, new_width, new_height, output_path):
    image = Image.open(image_path)
    # Resize the image
    resized_image = image.resize((new_width, new_height))
    # Save the resized image
    resized_image.save(output_path)

def show_image():
    selection = listbox.curselection()
    if selection:
        index = int(selection[len(selection) - 1])
        image_path = full_path_arr[index]
        if image_path.endswith(".svg"):
            drawing = svg2rlg(image_path)
            renderPM.drawToFile(drawing, "temp.png", fmt="PNG")
            image = Image.open('temp.png')
            photo = ImageTk.PhotoImage(image)
            image_label.config(image=photo)
            image_label.image = photo
            width, height = image.size
            dimensions_label.config(text=f"Dimensions: {width}x{height}")
        else:
            image = Image.open(image_path)
            image.thumbnail((300, 300))  # Resize the image if necessary
            photo = ImageTk.PhotoImage(image)
            image_label.config(image=photo)
            image_label.image = photo  # Store reference to avoid garbage collection
            width, height = image.size
            dimensions_label.config(text=f"Dimensions: {width}x{height}")

def show_image_added(event):
    selection = added_icons_listbox.curselection()
    if selection:
        index = int(selection[0])
        image_path = added_icons_arr[index]
        if image_path.endswith(".svg"):
            drawing = svg2rlg(image_path)
            renderPM.drawToFile(drawing, "temp.png", fmt="PNG")
            image = Image.open('temp.png')
            photo = ImageTk.PhotoImage(image)
            image_label.config(image=photo)
            image_label.image = photo
            width, height = image.size
            dimensions_label.config(text=f"Dimensions: {width}x{height}")
        else:
            image = Image.open(image_path)
            image.thumbnail((300, 300))  # Resize the image if necessary
            photo = ImageTk.PhotoImage(image)
            image_label.config(image=photo)
            image_label.image = photo  # Store reference to avoid garbage collection
            width, height = image.size
            dimensions_label.config(text=f"Dimensions: {width}x{height}")

def resize_image():
    try:
        # Get the selected image path
        selection = listbox.curselection()
        index = int(selection[len(selection) - 1])
        image_path = listbox.get(index)

        # Get the desired resolution
        new_width = int(width_entry.get())
        new_height = int(height_entry.get())

        # Open a file dialog to select a save location for the resized image
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=(("PNG File", "*.png"), ("All Files", "*.*")))
        # Change the resolution of the image and save the resized image
        change_resolution(image_path, new_width, new_height, output_path)
        result_label.config(text="Image Resized and Saved!")
    except Exception as e:
        result_label.config(text="An error occurred: " + str(e))

def resize_image_added():
    try:
        selection = added_icons_listbox.curselection()
        image_path = added_icons_listbox.get(selection)

        new_width = int(width_entry.get())
        new_height = int(height_entry.get())

        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=(("PNG File", "*.png"), ("All Files", "*.*")))
        change_resolution(image_path, new_width, new_height, output_path)
        result_label.config(text="Image Resized and Saved!")
    except Exception as e:
        result_label.config(text="An error occurred: " + str(e))

def ignore_click(event):
    return "break"

def select_all():
    listbox.select_set(0, tk.END)
    update_selected_list()

def unselect_all():
    listbox.selection_clear(0, tk.END)
    update_selected_list()

def find_icons_in_files(folder_path):
    icons = []
    file_paths = glob.glob(os.path.join(folder_path, "**/*.cpp"), recursive=True) + \
                 glob.glob(os.path.join(folder_path, "**/*.cc"), recursive=True) + \
                 glob.glob(os.path.join(folder_path, "**/*.cxx"), recursive=True) + \
                 glob.glob(os.path.join(folder_path, "**/*.ui"), recursive=True)
    #modify this to search for different files
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            source_code = file.read()
            lines = source_code.split('\n')
                
            for line in lines:
                #modify this to look for icons in different format
                if 'QIcon::fromTheme' in line:
                    icon_name = line.split('::fromTheme("')[1].split('")')[0]
                    icons.append(icon_name)
                if 'iconset theme=' in line:
                    icon_name = line.split('theme="')[1].split('"')[0]
                    icons.append(icon_name)
    for file in icons:
         if not file in names_to_match:
            names_to_match.append(file)
            update_array()
    return icons

def ask_directory_with_create_new_folder():
    # Run the zenity command to open the folder selection dialog
    result = subprocess.run(["zenity", "--file-selection", "--directory", "--title=Select Directory"], capture_output=True, text=True)

    if result.returncode == 0:
        # Extract the selected directory from the command output
        selected_directory = result.stdout.strip()
        return selected_directory
    else:
        # Return None if the user canceled the dialog
        return None

window = tk.Tk()
window.title("ICON File Copy")
window.geometry("900x900")

source_label = tk.Label(window, text="Source Folder:")
source_label.pack()
source_entry = tk.Entry(window, width=40)
source_entry.pack()

destination_label = tk.Label(window, text="Destination Folder:")
destination_label.pack()
destination_entry = tk.Entry(window, width=40)
destination_entry.pack()

source_code_label = tk.Label(window, text="Source code Folder:")
source_code_label.pack()
source_code_entry = tk.Entry(window, width=40)
source_code_entry.pack()




# Create buttons
source_button = tk.Button(window, text="Browse source", command=browse_source_folder)
source_button.pack()

destination_button = tk.Button(window, text="Browse destination", command=browse_destination_folder)
destination_button.pack()

source_code_button = tk.Button(window, text="Browse code", command=browse_source_code_folder)
source_code_button.pack()


# index theme
array_label = tk.Label(window, text="")
array_label.pack()

# Create and configure the entry widget
entry = tk.Entry(window)
entry.pack()

# Create and configure the push button
push_button = tk.Button(window, text="Push Item", command=push_item)
push_button.pack()

copy_button2 = tk.Button(window, text="Copy all from source", command=copyfiles)
copy_button2.pack()

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
select_all_button = tk.Button(window, text="select all", command=select_all)
select_all_button.pack()
unselect_all_button = tk.Button(window, text="unselect", command=unselect_all)
unselect_all_button.pack()

window.bind("<Return>", (lambda event: search_files()))

# Create listbox to display SVG files
listbox_frame = tk.Frame(window)
listbox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

listbox_scrollbar = Scrollbar(listbox_frame, orient=tk.VERTICAL)
listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = Listbox(listbox_frame, selectmode=MULTIPLE,font=("Helvetica",8),exportselection=0)
listbox.pack(fill=tk.BOTH, expand=True)
listbox.config(yscrollcommand=listbox_scrollbar.set)
listbox_scrollbar.config(command=listbox.yview)

# Create listbox to display selected SVG files
selected_frame = tk.Frame(window)
selected_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

selected_listbox_scrollbar = Scrollbar(selected_frame, orient=tk.VERTICAL)
selected_listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

selected_listbox = Listbox(selected_frame)
selected_listbox.pack(fill=tk.BOTH, expand=True)
selected_listbox.config(yscrollcommand=selected_listbox_scrollbar.set)
selected_listbox_scrollbar.config(command=selected_listbox.yview)
selected_listbox.bind("<Button-1>", ignore_click)

# destination folder list update_added_icons_list(destination_folder)
added_icons_frame = tk.Frame(window)
added_icons_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

added_icons_scrollbar = Scrollbar(added_icons_frame, orient=tk.VERTICAL)
added_icons_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

added_icons_listbox = Listbox(added_icons_frame)
added_icons_listbox.pack(fill=tk.BOTH, expand=True)
added_icons_listbox.config(yscrollcommand=added_icons_scrollbar.set)
added_icons_scrollbar.config(command=added_icons_listbox.yview)
added_icons_listbox.bind("<<ListboxSelect>>",show_image_added)

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

image_label = Label(window)
image_label.pack()

dimensions_label = Label(window, text="current dimensions")
dimensions_label.pack()

width_label = Label(window, text="New Width:")
width_label.pack()
width_entry = Entry(window)
width_entry.pack()

height_label = Label(window, text="New Height:")
height_label.pack()
height_entry = Entry(window)
height_entry.pack()

resize_button = Button(window, text="Resize Image", command=resize_image)
resize_button.pack()

resize_button_added = Button(window, text="if in destination", command=resize_image_added)
resize_button_added.pack()

window.mainloop()
