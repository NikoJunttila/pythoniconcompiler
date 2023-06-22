from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel ,QComboBox, QFileDialog, QListView
from PyQt6.QtGui import QStandardItemModel, QIcon, QStandardItem,QFont, QPixmap
from PyQt6.QtCore import Qt, QSize
from pathlib import Path
import glob
import os
import shutil
from PIL import Image


#global variables
names_to_match = [] 
check_all_found = []

def get_icon_resolution(file_path):
    try:
        if file_path.endswith(".svg"):
            #tbh idk about this fr fr
            return "work in progress"
        else:
            with Image.open(file_path) as img:
                width, height = img.size
                resolution = f"{width}x{height}"
                return resolution
    except (IOError, OSError):
        #print(OSError)
        return None

def get_svg_files(folder_path, search_term=None):
        svg_files = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith((".svg", ".png", ".jpg", ".jpeg")):
                    if search_term is None or search_term.lower() in file.lower():
                        svg_files.append(os.path.join(root, file))
        return svg_files

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
            check_all_found.append(file)

def get_themes(folder_path, search_term=None):
    themes = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".theme"):
                if search_term is None or search_term.lower() in file.lower():
                    themes.append(os.path.join(root, file))
    return themes



class ListView_Left(QListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.m_model = QStandardItemModel(self)
        self.setModel(self.m_model)
        self.setIconSize(QSize(50, 50))
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setViewMode(QListView.ViewMode.IconMode)



class ListView_Right(QListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.m_model = QStandardItemModel(self)
        self.setModel(self.m_model)
        self.setIconSize(QSize(50, 50))
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setViewMode(QListView.ViewMode.IconMode)
        #self.clicked.connect(self.on_item_clicked)  # Connect the clicked signal to the slot

    def on_item_clicked(self, index):
        item = self.m_model.itemFromIndex(index)
        if item is not None:
            print("Clicked item data:", item.text())

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(837, 619)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        font = QFont()
        font.setPointSize(7)
        self.src_code_2 = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.src_code_2.setGeometry(QtCore.QRect(0, 70, 841, 521))
        self.src_code_2.setObjectName("src_code_2")
        self.src_code = QtWidgets.QWidget()
        self.src_code.setObjectName("src_code")
        self.listWidget = ListView_Right(parent=self.src_code)
        self.listWidget.setGeometry(QtCore.QRect(520, 50, 301, 381))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setFont(font)
        self.src_code_folder = QtWidgets.QLineEdit(parent=self.src_code)
        self.src_code_folder.setGeometry(QtCore.QRect(50, 50, 201, 22))
        self.src_code_folder.setObjectName("src_code_folder")
        self.src_code_search = QtWidgets.QPushButton(parent=self.src_code)
        self.src_code_search.setGeometry(QtCore.QRect(110, 80, 75, 24))
        self.src_code_search.setObjectName("src_code_search")
        self.listWidget_2 = QtWidgets.QListWidget(parent=self.src_code)
        self.listWidget_2.setGeometry(QtCore.QRect(10, 150, 301, 241))
        self.listWidget_2.setObjectName("listWidget_2")
        self.label = QtWidgets.QLabel(parent=self.src_code)
        self.label.setGeometry(QtCore.QRect(80, 120, 140, 16))
        self.label.setObjectName("label")
        self.src_code_add = QtWidgets.QLineEdit(parent=self.src_code)
        self.src_code_add.setGeometry(QtCore.QRect(10, 410, 181, 22))
        self.src_code_add.setObjectName("src_code_add")
        self.src_code_add_btn = QtWidgets.QPushButton(parent=self.src_code)
        self.src_code_add_btn.setGeometry(QtCore.QRect(210, 410, 101, 24))
        self.src_code_add_btn.setObjectName("src_code_add_btn")
        self.copy_src_code = QtWidgets.QPushButton(parent=self.src_code)
        self.copy_src_code.setGeometry(QtCore.QRect(360, 150, 81, 241))
        self.copy_src_code.setObjectName("copy_src_code")
        self.label_2 = QtWidgets.QLabel(parent=self.src_code)
        self.label_2.setGeometry(QtCore.QRect(540, 20, 241, 20))
        self.label_2.setObjectName("label_2")
        self.src_code_2.addTab(self.src_code, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.listWidget_3 = ListView_Left(parent=self.tab_3)
        self.listWidget_3.setGeometry(QtCore.QRect(0, 70, 291, 251))
        self.listWidget_3.setObjectName("listWidget_3")
        self.listWidget_3.setFont(font)
        self.comboBox = QtWidgets.QComboBox(parent=self.tab_3)
        self.comboBox.setGeometry(QtCore.QRect(130, 320, 69, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.src_reso_label = QLabel(self.src_code)
        self.src_reso_label.setObjectName(u"src_reso_label")
        self.src_reso_label.setGeometry(QtCore.QRect(350, 90, 111, 16))
        self.src_code_resolution = QComboBox(self.src_code)
        self.src_code_resolution.addItem("")
        self.src_code_resolution.addItem("")
        self.src_code_resolution.addItem("")
        self.src_code_resolution.addItem("")
        self.src_code_resolution.addItem("")
        self.src_code_resolution.addItem("")
        self.src_code_resolution.addItem("")
        self.src_code_resolution.addItem("")
        self.src_code_resolution.addItem("")
        self.src_code_resolution.addItem("")
        self.src_code_resolution.addItem("")
        self.src_code_resolution.setObjectName(u"src_code_resolution")
        self.src_code_resolution.setGeometry(QtCore.QRect(360, 110, 81, 22))
        self.label_3 = QtWidgets.QLabel(parent=self.tab_3)
        self.label_3.setGeometry(QtCore.QRect(50, 320, 100, 20))
        self.label_3.setObjectName("label_3")
        self.select_all = QtWidgets.QPushButton(self.tab_3)
        self.select_all.setObjectName(u"select_all")
        self.select_all.setGeometry(QtCore.QRect(210, 40, 75, 24))
        self.listWidget_4 = ListView_Left(parent=self.tab_3)
        self.listWidget_4.setGeometry(QtCore.QRect(0, 370, 291, 111))
        self.listWidget_4.setObjectName("listWidget_4")
        self.search_text = QtWidgets.QLineEdit(parent=self.tab_3)
        self.search_text.setGeometry(QtCore.QRect(0, 10, 181, 22))
        self.search_text.setObjectName("search_text")
        self.search_btn = QtWidgets.QPushButton(parent=self.tab_3)
        self.search_btn.setGeometry(QtCore.QRect(190, 10, 75, 24))
        self.search_btn.setObjectName("search_btn")
        self.img_name = QtWidgets.QLabel(parent=self.tab_3)
        self.img_name.setGeometry(QtCore.QRect(300, 250, 231, 20))
        self.img_name.setObjectName("img_name")
        self.img_size = QtWidgets.QLabel(parent=self.tab_3)
        self.img_size.setGeometry(QtCore.QRect(370, 320, 181, 20))
        self.img_size.setObjectName("img_size")
        self.copy_selected_btn = QtWidgets.QPushButton(parent=self.tab_3)
        self.copy_selected_btn.setGeometry(QtCore.QRect(350, 370, 141, 81))
        self.copy_selected_btn.setObjectName("copy_selected_btn")
        self.listWidget_5 = ListView_Right(parent=self.tab_3)
        self.listWidget_5.setGeometry(QtCore.QRect(570, 40, 256, 441))
        self.listWidget_5.setObjectName("listWidget_5")
        self.listWidget_5.setFont(font)
        self.label_6 = QtWidgets.QLabel(parent=self.tab_3)
        self.label_6.setGeometry(QtCore.QRect(580, 10, 261, 20))
        self.label_6.setObjectName("label_6")
        self.image_loader = QtWidgets.QLabel(parent=self.tab_3)
        self.image_loader.setGeometry(QtCore.QRect(300, 10, 231, 231))
        self.image_loader.setObjectName("image_loader")
        self.label_8 = QtWidgets.QLabel(parent=self.tab_3)
        self.label_8.setGeometry(QtCore.QRect(80, 350, 110, 16))
        self.label_8.setObjectName("label_8")
        self.src_code_2.addTab(self.tab_3, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.src_code_2.addTab(self.tab_2, "")
        self.clear_selected_btn = QtWidgets.QPushButton(self.tab_3)
        self.clear_selected_btn.setObjectName(u"clear_selected_btn")
        self.clear_selected_btn.setGeometry(QtCore.QRect(160, 345, 75, 24))
        self.icons_folder = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.icons_folder.setGeometry(QtCore.QRect(10, 20, 201, 22))
        self.icons_folder.setObjectName("icons_folder")
        self.destination_folder = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.destination_folder.setGeometry(QtCore.QRect(510, 20, 201, 22))
        self.destination_folder.setObjectName("destination_folder")
        self.icons_folder_btn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.icons_folder_btn.setGeometry(QtCore.QRect(230, 20, 100, 24))
        self.icons_folder_btn.setObjectName("icons_folder_btn")
        self.destination_folder_btn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.destination_folder_btn.setGeometry(QtCore.QRect(730, 20, 100, 24))
        self.destination_folder_btn.setObjectName("destination_folder_btn")
        self.copy_resolution = QComboBox(self.tab_3)
        self.copy_resolution.addItem("")
        self.copy_resolution.addItem("")
        self.copy_resolution.addItem("")
        self.copy_resolution.addItem("")
        self.copy_resolution.addItem("")
        self.copy_resolution.addItem("")
        self.copy_resolution.addItem("")
        self.copy_resolution.addItem("")
        self.copy_resolution.addItem("")
        self.copy_resolution.addItem("")
        self.copy_resolution.addItem("")
        self.copy_resolution.setObjectName(u"copy_resolution")
        self.copy_resolution.setGeometry(QtCore.QRect(0, 40, 81, 21))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 837, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        #connect stuff
        self.src_code_search.clicked.connect(self.choose_src_code_directory)
        self.src_code_add_btn.clicked.connect(self.add_name)
        self.icons_folder_btn.clicked.connect(self.choose_icons_directory)
        self.destination_folder_btn.clicked.connect(self.choose_destination_directory)
        self.comboBox.currentIndexChanged.connect(self.loadIcons)
        self.copy_src_code.clicked.connect(self.copyfiles)
        self.search_btn.clicked.connect(self.loadIcons)
        self.copy_resolution.currentIndexChanged.connect(self.loadIcons)
        self.listWidget_3.clicked.connect(self.on_item_clicked_main)
        self.listWidget_4.clicked.connect(self.delete_item)
        self.clear_selected_btn.clicked.connect(self.clear_selected)
        self.select_all.clicked.connect(self.select_all_func)
        
        self.retranslateUi(MainWindow)
        self.src_code_2.setCurrentIndex(1)
        self.comboBox.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #self.search_text.keyPressEvent = self.keyPressEvent

    #def keyPressEvent(self, event):
       # if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
       #     self.search_btn.click()

    def on_item_clicked_main(self, index):
        try:
            item = self.listWidget_3.m_model.itemFromIndex(index)
            data = item.data()
            file_name = os.path.basename(data)
            pixmap = QPixmap(data)
            self.image_loader.setPixmap(pixmap)
            item2 = QStandardItem()
            item2.setIcon(QIcon(data))
            item2.setData(data)
            self.listWidget_4.m_model.appendRow(item2)
            icon_resolution = get_icon_resolution(data)
            self.img_size.setText(icon_resolution)
            self.img_name.setText(file_name)
        except Exception as e:
            print("An error occurred: " + str(e))

    def clear_selected(self):
        self.listWidget_4.m_model.clear()

    def delete_item(self, item):
        row = item.row()
        self.listWidget_4.m_model.removeRow(row)

    def select_all_func(self):
        for row in range(self.listWidget_3.m_model.rowCount()):
            index = self.listWidget_3.m_model.index(row,0)
            try:
                item = self.listWidget_3.m_model.itemFromIndex(index)
                data = item.data()
                item2 = QStandardItem()
                item2.setData(data)
                item2.setIcon(QIcon(data))
                self.listWidget_4.m_model.appendRow(item2)
            except Exception as e:
                print("An error occurred: " + str(e))

    def loadIcons_dest(self, path):
        icons = get_svg_files(path)
        self.listWidget.m_model.clear()
        for index, icon in enumerate(icons):
            if index >= 100:
                break
            item = QStandardItem()
            item.setIcon(QIcon(icon))
            file_name = os.path.basename(icon)
            split_name = file_name.split(".")[0]
            item.setText(split_name)
            self.listWidget.m_model.appendRow(item)
            
    def loadIcons_dest2(self, path):
        icons = get_svg_files(path)
        self.listWidget_5.m_model.clear()
        for index, icon in enumerate(icons):
            if index >= 100:
                break
            item = QStandardItem()
            item.setIcon(QIcon(icon))
            file_name = os.path.basename(icon)
            split_name = file_name.split(".")[0]
            item.setText(split_name)
            self.listWidget_5.m_model.appendRow(item)

    def loadIcons(self):
        search_term = self.search_text.text()
        folder_path = self.icons_folder.text()
        resolution_check = self.copy_resolution.currentText()
        if resolution_check == "None":
            resolution_check = None
        if len(folder_path) > 2:
            if not os.path.exists(folder_path):
                print("Source folder '{folder_path}' does not exist.")
                return
            icons = get_svg_files(folder_path, search_term)
            self.listWidget_3.m_model.clear()
            number = int(self.comboBox.currentText())
            loop_count = 0
            if resolution_check:
                for icon in icons:
                    if loop_count >= number:
                        break
                    icon_resolution = get_icon_resolution(icon)
                    if icon_resolution == resolution_check or icon_resolution == "work in progress" :
                        item = QStandardItem()
                        item.setIcon(QIcon(icon))
                        item.setData(icon)
                        file_name = os.path.basename(icon)
                        split_name = file_name.split(".")[0]
                        item.setText(split_name)
                        self.listWidget_3.m_model.appendRow(item)
                        loop_count += 1
            else: 
                for icon in icons:
                    if loop_count >= number:
                        break
                    item = QStandardItem()
                    item.setIcon(QIcon(icon))
                    item.setData(icon)
                    file_name = os.path.basename(icon)
                    split_name = file_name.split(".")[0]
                    item.setText(split_name)
                    self.listWidget_3.m_model.appendRow(item)
                    loop_count += 1

    def choose_icons_directory(self):
        dir_name = QFileDialog.getExistingDirectory(self.centralwidget, "Select a Directory")
        if dir_name:
            path = Path(dir_name)
            self.icons_folder.setText(str(path))
            self.loadIcons()
    
    def choose_destination_directory(self):
        dir_name = QFileDialog.getExistingDirectory(self.centralwidget, "Select a Directory")
        if dir_name:
            path = Path(dir_name)
            self.destination_folder.setText(str(path))
            self.loadIcons_dest(path)
            self.loadIcons_dest2(path)


    def choose_src_code_directory(self):
        dir_name = QFileDialog.getExistingDirectory(self.centralwidget, "Select a Directory")
        if dir_name:
            path = Path(dir_name)
            self.src_code_folder.setText(str(path))
            find_icons_in_files(dir_name)
            for icon in names_to_match:
                self.listWidget_2.addItem(icon)
                
    def add_name(self):
        name = self.src_code_add.text()
        if name:
            names_to_match.append(name)
            self.listWidget_2.addItem(name)
            self.src_code_add.clear()



    def copyfiles(self):
        source_folder = self.icons_folder.text()
        destination_folder = self.destination_folder.text()
        svg_files = get_svg_files(source_folder) 
        index_themes = get_themes(source_folder)  
        src_code = self.src_code_folder.text()
        find_icons_in_files(src_code)
        resolution_check = self.src_code_resolution.currentText()
        if resolution_check == "None":
            resolution_check = None

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
                
                if split_name in names_to_match:
                    relative_path = os.path.relpath(file, source_folder)
                    icon_resolution = get_icon_resolution(file)
                    if resolution_check:
                        if icon_resolution == resolution_check or icon_resolution == "work in progress":
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
            self.loadIcons_dest(destination_folder)
            self.loadIcons_dest2(destination_folder)
            if len(check_all_found) > 0:
                print("files not found:")
                for file in check_all_found:
                    print(file)
            else:
                print("found all icons needed!")
        except Exception as e:
            print("An error occurred: " + str(e))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.src_code_2.setToolTip(_translate("MainWindow", "<html><head/><body><p>src code</p></body></html>"))
        self.src_code_2.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>src code</p><p><br/></p></body></html>"))
        self.src_code_search.setText(_translate("MainWindow", "src code"))
        self.label.setText(_translate("MainWindow", "Found icon names:"))
        self.src_code_add_btn.setText(_translate("MainWindow", "add icon"))
        self.copy_src_code.setText(_translate("MainWindow", "Copy icons"))
        self.label_2.setText(_translate("MainWindow", "Icons in destination folder"))
        self.src_code_2.setTabText(self.src_code_2.indexOf(self.src_code), _translate("MainWindow", "src_code"))
        self.comboBox.setItemText(0, _translate("MainWindow", "10"))
        self.comboBox.setItemText(1, _translate("MainWindow", "25"))
        self.comboBox.setItemText(2, _translate("MainWindow", "50"))
        self.comboBox.setItemText(3, _translate("MainWindow", "100"))
        self.comboBox.setItemText(4, _translate("MainWindow", "200"))
        self.comboBox.setItemText(5, _translate("MainWindow", "500"))
        self.comboBox.setItemText(6, _translate("MainWindow", "1000"))
        self.src_code_resolution.setItemText(0,  _translate("MainWindow", u"None", None))
        self.src_code_resolution.setItemText(1,  _translate("MainWindow", u"8x8", None))
        self.src_code_resolution.setItemText(2,  _translate("MainWindow", u"12x12", None))
        self.src_code_resolution.setItemText(3,  _translate("MainWindow", u"16x16", None))
        self.src_code_resolution.setItemText(4,  _translate("MainWindow", u"22x22", None))
        self.src_code_resolution.setItemText(5,  _translate("MainWindow", u"24x24", None))
        self.src_code_resolution.setItemText(6,  _translate("MainWindow", u"32x32", None))
        self.src_code_resolution.setItemText(7,  _translate("MainWindow", u"48x48", None))
        self.src_code_resolution.setItemText(8,  _translate("MainWindow", u"64x64", None))
        self.src_code_resolution.setItemText(9,  _translate("MainWindow", u"128x128", None))
        self.src_code_resolution.setItemText(10,  _translate("MainWindow", u"256x256", None))
        self.label_3.setText(_translate("MainWindow", "Icons loaded"))
        self.search_btn.setText(_translate("MainWindow", "Search"))
        self.img_name.setText(_translate("MainWindow", ""))
        self.img_size.setText(_translate("MainWindow", ""))
        self.copy_selected_btn.setText(_translate("MainWindow", "Copy selected"))
        self.label_6.setText(_translate("MainWindow", "Icons in destination folder"))
        self.image_loader.setText(_translate("MainWindow", ""))
        self.label_8.setText(_translate("MainWindow", "selected icons:"))
        self.select_all.setText(_translate("MainWindow", u"Select all"))
        self.clear_selected_btn.setText(_translate("MainWindow", u"Clear"))
        self.src_code_2.setTabText(self.src_code_2.indexOf(self.tab_3), _translate("MainWindow", "copy"))
        self.src_code_2.setTabText(self.src_code_2.indexOf(self.tab_2), _translate("MainWindow", "theme gen"))
        self.icons_folder_btn.setText(_translate("MainWindow", "Icons folder"))
        self.copy_resolution.setItemText(0, _translate("MainWindow", u"None", None))
        self.copy_resolution.setItemText(1, _translate("MainWindow", u"8x8", None))
        self.copy_resolution.setItemText(2, _translate("MainWindow", u"12x12", None))
        self.copy_resolution.setItemText(3, _translate("MainWindow", u"16x16", None))
        self.copy_resolution.setItemText(4, _translate("MainWindow", u"22x22", None))
        self.copy_resolution.setItemText(5, _translate("MainWindow", u"24x24", None))
        self.copy_resolution.setItemText(6, _translate("MainWindow", u"32x32", None))
        self.copy_resolution.setItemText(7, _translate("MainWindow", u"48x48", None))
        self.copy_resolution.setItemText(8, _translate("MainWindow", u"64x64", None))
        self.copy_resolution.setItemText(9, _translate("MainWindow", u"128x128", None))
        self.copy_resolution.setItemText(10, _translate("MainWindow", u"256x256", None))
        self.src_reso_label.setText(_translate("MainWindow", u"Limit icons size"))
        self.destination_folder_btn.setText(_translate("MainWindow", "Destination"))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create an instance of the UI class
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()