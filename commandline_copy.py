import shutil
import os
import glob
import time

src_code = input("give src code folder \n")
icon_source = input("Give folder where to look for icons \n")
icon_destination = input("Give folder where to copy icons \n")

names_to_match = [] 


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
    print("icons found:")
    for file in icons:
         if not file in names_to_match:
            names_to_match.append(file)
            print(file)
            time.sleep(100/1000)
    return icons

def copyfiles():
    source_folder = icon_source
    destination_folder = icon_destination
    svg_files = get_svg_files(source_folder) 
    index_themes = get_themes(source_folder)  
    find_icons_in_files(src_code)

    try:
        # Check if the source folder exists
        if not os.path.exists(source_folder):
            print("invalid icon src path")
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
        print("copied succesfully")
    except Exception as e:
        print("An error occurred: " + str(e))

copyfiles()