# pythoniconcompiler
<b>Compile huge icon sets in to smaller sets.</b> </br>
to try out this app do: </br>
pip install -r requirements.txt  </br>
you can use cmd_arg_copy.py for fast copy. </br>
Give 3 arguments 1. src-code folder, icons src folder, destination folder (creates if doesn't exist already). example: </br>
python cmd_arg_copy.py src-code-folder icons-src-folder destination </br>
or use auto_dest_copy.py that takes 2 arguments src-code folder and icons src folder. then generates icons folder to src-code folder where it copies icons example: (optional 3rd argument for icon size.) </br>
python auto_dest_copy.py src-code-folder-path icons-src-folder-path 32,64,16x64 would select 32x32,64x64 and 16x64 icon sizes</br>
src code search made for Qt cpp/py projects and doesnt work if done with `` instead of "" </br>
