# pythoniconcompiler
<b>Compile huge icon sets in to smaller sets.</b> </br>
comparison image shows difference between full size icon set folder and smaller icon set with only icons necessary for project. </br>
to try out this app do command for gui: </br>
pip install -r requirements.txt  </br>
you can also use cmd_arg_copy.py for fast copy.  </br>
Give 3 arguments 1. src-code folder, icons src folder, destination folder (creates if doesnt exist already). example: </br>
python cmd_arg_copy.py src-code-folder icons-src-folder destination </br>
or use auto_dest_copy.py that takes 2 arguments src-code folder and icons src folder. then generates icons folder to src-code folder where it copies icons example: (optional 3rd argument for icon size. doesn't work for svg yet) </br>
python auto_dest_copy.py src-code-folder-path icons-src-folder-path 32x32</br>
src code search made for Qt projects and doesnt work if done with `` instead of "" </br>
icon size change doesnt work for svg icons atm 
