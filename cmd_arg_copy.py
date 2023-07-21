import shutil
import os
import glob
import sys
from PIL import Image
from PyQt6.QtSvg import QSvgRenderer
import copy

src_code = sys.argv[1]
icon_source = sys.argv[2]
icon_destination = sys.argv[3]
try:
  resolution_check = sys.argv[4]
except IndexError:
  resolution_check = None

def make_array_resolutions(string):
    try:
        array = string.split(",")
        for i in range(len(array)):
            if not "x" in str(array[i]):
                array[i] = f"{array[i]}x{array[i]}"
        return array
    except:
        print("no string to parse")

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
    #modify this to search for different files
    file_paths = glob.glob(os.path.join(folder_path, "**/*.cpp"), recursive=True) + \
                 glob.glob(os.path.join(folder_path, "**/*.cc"), recursive=True) + \
                 glob.glob(os.path.join(folder_path, "**/*.cxx"), recursive=True) + \
                 glob.glob(os.path.join(folder_path, "**/*.ui"), recursive=True) + \
                 glob.glob(os.path.join(folder_path, "**/*.py"), recursive=True)
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            source_code = file.read()
            lines = source_code.split('\n')
                
            for line in lines:
                try:
                    #modify this to look for icons in different format
                    if 'QIcon::fromTheme' in line:
                        icon_name = line.split('::fromTheme("')[1].split('")')[0]
                        if not icon_name in icons:
                            icons.append(icon_name)
                    if 'iconset theme=' in line:
                        icon_name = line.split('theme="')[1].split('"')[0]
                        if not icon_name in icons:
                            icons.append(icon_name)
                    if 'QIcon' in line:
                        icon_name = line.split('QIcon("')[1].split('.')[0]
                        parsed_string = icon_name.split("/")[-1]
                        if not parsed_string in icons:
                            icons.append(parsed_string)
                    if 'QPixmap' in line:
                        icon_name = line.split('QPixmap("')[1].split('.')[0]
                        parsed_string = icon_name.split("/")[-1]
                        if not parsed_string in icons:
                            icons.append(parsed_string)
                except:
                    continue
    print("icons found:")
    for file in icons:
            print(file)
    return icons


def get_next_character_after_at(string):
    at_index = string.find('@')
    if at_index != -1 and at_index < len(string) - 1:
        return string[at_index + 1]
    else:
        return None

def get_icon_resolution(file_path):
    try:
        if file_path.endswith(".svg"):
            renderer = QSvgRenderer()
            if renderer.load(file_path):
                # Get the default size of the SVG file
                default_size = renderer.defaultSize()
                resolution = f"{default_size.width()}x{default_size.height()}"
                return resolution
            else:
                return "error"
        else:
            with Image.open(file_path) as img:
                width, height = img.size
            #lets hope u dont have multiple @ in ur path
                if "@" in file_path:
                    divider = get_next_character_after_at(file_path)
                    if divider == "2" or divider == "3" or divider == "4":
                        divider = int(divider)
                        resolution = f"{int(width/divider)}x{int(height/divider)}"
                    else:
                        resolution = f"{width}x{height}"
                    return resolution
                else: 
                    resolution = f"{width}x{height}"
                    return resolution
    except (IOError, OSError):
        #print(OSError)
        return None

def copyfiles():
    source_folder = icon_source
    destination_folder = icon_destination
    svg_files = get_svg_files(source_folder) 
    index_themes = get_themes(source_folder)  
    icons = find_icons_in_files(src_code)
    check_all_found = copy.deepcopy(icons)
    needed_resolutions = None 
    if resolution_check:
        needed_resolutions = make_array_resolutions(resolution_check)

    try:
        if not os.path.exists(source_folder):
            print("invalid icon src path")
            return

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        for file in index_themes:
            file_name = os.path.basename(file)
            relative_path = os.path.relpath(file, source_folder)

            destination_subfolder = os.path.dirname(os.path.join(destination_folder, relative_path))
            os.makedirs(destination_subfolder, exist_ok=True)

            destination_path = os.path.join(destination_subfolder, os.path.basename(file))

            if not os.path.exists(destination_path):
                shutil.copy(file, destination_path)

        for file in svg_files:
            file_name = os.path.basename(file)
            split_name = file_name.split(".")[0]
            
            if split_name in icons:
                relative_path = os.path.relpath(file, source_folder)
                icon_resolution = get_icon_resolution(file)
                if resolution_check:
                    if icon_resolution in needed_resolutions:
                        destination_subfolder = os.path.dirname(os.path.join(destination_folder, relative_path))
                        os.makedirs(destination_subfolder, exist_ok=True)
                        destination_path = os.path.join(destination_subfolder, os.path.basename(file))
                        shutil.copy(file, destination_path)
                        if split_name in check_all_found:
                            check_all_found.remove(split_name)
                else:
                    destination_subfolder = os.path.dirname(os.path.join(destination_folder, relative_path))
                    os.makedirs(destination_subfolder, exist_ok=True)
                    destination_path = os.path.join(destination_subfolder, os.path.basename(file))
                    shutil.copy(file, destination_path)
                    if split_name in check_all_found:
                        check_all_found.remove(split_name)

        print("copied succesfully!")
        if len(check_all_found) > 0:
            print("files not found:")
            for file in check_all_found:
                print(file)
        else:
            print("found all icons needed!")
    except Exception as e:
        print("An error occurred: " + str(e))

copyfiles()