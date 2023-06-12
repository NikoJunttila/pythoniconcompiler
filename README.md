# pythoniconcompiler
Compile huge icon sets in to smaller sets.
comparison image shows difference between full size icon set folder and smaller icon set with only icons necessary for project.
to try out this app do command for gui:
pip install -r requirements.txt
you can also use cmd_arg_copy.py for fast copy
Give 3 arguments 1. src-code folder, icons src folder, destination folder (creates if doesnt exist already). example:
python cmd_arg_copy.py src-code-folder icons-src-folder destination
or use auto_dest_copy.py that takes 2 arguments src-code folder and icons src folder. then generates icons folder to src-code folder where it copies icons example:
python auto_dest_copy.py src-code-folder-path icons-src-folder-path
