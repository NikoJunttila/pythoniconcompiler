from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel ,QComboBox, QFileDialog, QListView,
    QMessageBox, QWidget, QLineEdit, QVBoxLayout, QCheckBox)
from PyQt6.QtGui import QStandardItemModel, QIcon, QStandardItem,QFont, QPixmap, QMovie, QAction
from PyQt6.QtCore import Qt, QSize, QEvent, QRunnable, pyqtSlot, QThreadPool
from PyQt6.QtSvg import QSvgRenderer
from pathlib import Path
import glob
import os
import shutil
from PIL import Image
from PyQt6 import QtCore, QtGui, QtWidgets

names_to_match = [] 
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
        return None
    
def get_themes(folder_path, search_term=None):
    themes = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".theme"):
                if search_term is None or search_term.lower() in file.lower():
                    themes.append(os.path.join(root, file))
    return themes

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


def get_all_resolutions(path):
    icons = get_svg_files(path)
    resolutions = []
    
    thread_pool = QThreadPool.globalInstance()
    for icon in icons:
        worker = ResolutionWorker(icon, resolutions)
        worker.setAutoDelete(True)
        thread_pool.start(worker)
    
    thread_pool.waitForDone()
    
    return resolutions

class ResolutionWorker(QRunnable):
    def __init__(self, icon, resolutions):
        super().__init__()
        self.icon = icon
        self.resolutions = resolutions
    
    def run(self):
        resolution = get_icon_resolution(self.icon)
        if resolution not in self.resolutions:
            self.resolutions.append(resolution)

class LoadIconsWorker(QRunnable):
    def __init__(self, folder_path, search_term, resolution_check, number,categories_check, ui):
        super().__init__()
        self.folder_path = folder_path
        self.search_term = search_term
        self.resolution_check = resolution_check
        self.number = number
        self.ui = ui
        self.categories_check = categories_check

    @pyqtSlot()
    def run(self):
        self.ui.showLoadingSpinner(True)

        icons = get_svg_files(self.folder_path, self.search_term)
        self.ui.listWidget_3.m_model.clear()
        loop_count = 0
        if self.resolution_check and self.categories_check:
            for icon in icons:
                if loop_count >= self.number:
                    break
                icon_resolution = get_icon_resolution(icon)
                if icon_resolution == self.resolution_check and self.categories_check in icon:
                    item = QStandardItem()
                    item.setIcon(QIcon(icon))
                    item.setData(icon)
                    file_name = os.path.basename(icon)
                    split_name = file_name.split(".")[0]
                    item.setText(split_name)
                    self.ui.listWidget_3.m_model.appendRow(item)
                    loop_count += 1
        elif self.resolution_check:
            for icon in icons:
                if loop_count >= self.number:
                    break
                icon_resolution = get_icon_resolution(icon)
                if icon_resolution == self.resolution_check:
                    item = QStandardItem()
                    item.setIcon(QIcon(icon))
                    item.setData(icon)
                    file_name = os.path.basename(icon)
                    split_name = file_name.split(".")[0]
                    item.setText(split_name)
                    self.ui.listWidget_3.m_model.appendRow(item)
                    loop_count += 1
        elif self.categories_check:
            for icon in icons:
                if loop_count >= self.number:
                    break
                if self.categories_check in icon:
                    item = QStandardItem()
                    item.setIcon(QIcon(icon))
                    item.setData(icon)
                    file_name = os.path.basename(icon)
                    split_name = file_name.split(".")[0]
                    item.setText(split_name)
                    self.ui.listWidget_3.m_model.appendRow(item)
                    loop_count += 1
        else:
            for icon in icons:
                if loop_count >= self.number:
                    break
                item = QStandardItem()
                item.setIcon(QIcon(icon))
                item.setData(icon)
                file_name = os.path.basename(icon)
                split_name = file_name.split(".")[0]
                item.setText(split_name)
                self.ui.listWidget_3.m_model.appendRow(item)
                loop_count += 1
        if loop_count == 0:
            item = QStandardItem()
            item.setText("No icons found with this name or resolution")
            self.ui.listWidget_3.m_model.appendRow(item)
        self.ui.showLoadingSpinner(False)

class ListView_Left(QListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.m_model = QStandardItemModel(self)
        self.setModel(self.m_model)
        self.setIconSize(QSize(50, 50))
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setViewMode(QListView.ViewMode.IconMode)

class InputFieldWidget(QWidget):
    def __init__(self, on_enter_pressed=None, parent=None):
        super().__init__(parent)
        self.input_field = QLineEdit(self)
        #layout = QVBoxLayout(self)
        #layout.addWidget(self.input_field)
        self.input_field.installEventFilter(self)

        self.on_enter_pressed = on_enter_pressed

    def eventFilter(self, obj, event):
        if obj is self.input_field and event.type() == QEvent.Type.KeyPress:
            key = event.key()
            if key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
                if self.on_enter_pressed:
                    self.on_enter_pressed()
        return super().eventFilter(obj, event)

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
        MainWindow.resize(894, 754)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.icons_folder = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.icons_folder.setObjectName("icons_folder")
        self.horizontalLayout.addWidget(self.icons_folder)
        self.icons_folder_btn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.icons_folder_btn.setObjectName("icons_folder_btn")
        self.horizontalLayout.addWidget(self.icons_folder_btn)
        self.label_5 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.destination_folder = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.destination_folder.setObjectName("destination_folder")
        self.horizontalLayout.addWidget(self.destination_folder)
        self.destination_folder_btn = QtWidgets.QPushButton(parent=self.centralwidget)
        self.destination_folder_btn.setObjectName("destination_folder_btn")
        self.horizontalLayout.addWidget(self.destination_folder_btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.src_code_2 = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.src_code_2.setMinimumSize(QtCore.QSize(0, 300))
        self.src_code_2.setBaseSize(QtCore.QSize(0, 1000))
        self.src_code_2.setObjectName("src_code_2")
        self.src_code = QtWidgets.QWidget()
        self.src_code.setObjectName("src_code")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.src_code)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.src_code_folder = QtWidgets.QLineEdit(parent=self.src_code)
        self.src_code_folder.setObjectName("src_code_folder")
        self.gridLayout.addWidget(self.src_code_folder, 0, 0, 1, 2)
        self.src_code_search = QtWidgets.QPushButton(parent=self.src_code)
        self.src_code_search.setObjectName("src_code_search")
        self.gridLayout.addWidget(self.src_code_search, 1, 0, 1, 2)
        self.label = QtWidgets.QLabel(parent=self.src_code)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 2)
        self.listWidget_2 = QtWidgets.QListWidget(parent=self.src_code)
        self.listWidget_2.setObjectName("listWidget_2")
        self.gridLayout.addWidget(self.listWidget_2, 3, 0, 1, 2)
        self.src_code_add = InputFieldWidget(self.add_name,parent=self.src_code)
        self.src_code_add.setObjectName("src_code_add")
        self.gridLayout.addWidget(self.src_code_add, 4, 0, 1, 1)
        self.src_code_add_btn = QtWidgets.QPushButton(parent=self.src_code)
        self.src_code_add_btn.setObjectName("src_code_add_btn")
        self.gridLayout.addWidget(self.src_code_add_btn, 4, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.copy_src_code = QtWidgets.QPushButton(parent=self.src_code)
        self.copy_src_code.setObjectName("copy_src_code")
        self.gridLayout_2.addWidget(self.copy_src_code, 5, 0, 1, 2)
        self.horizontalLayout_2.addLayout(self.gridLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(parent=self.src_code)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.listWidget = ListView_Right(parent=self.src_code)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.src_code_2.addTab(self.src_code, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.search_text = InputFieldWidget(self.loadIcons,parent=self.tab_3)
        self.search_text.setObjectName("search_text")
        self.gridLayout_3.addWidget(self.search_text, 0, 0, 1, 2)
        self.search_btn = QtWidgets.QPushButton(parent=self.tab_3)
        self.search_btn.setObjectName("search_btn")
        self.gridLayout_3.addWidget(self.search_btn, 0, 2, 1, 1)
        self.copy_resolution = QtWidgets.QComboBox(parent=self.tab_3)
        self.copy_resolution.setObjectName("copy_resolution")
        self.copy_resolution.addItem("")
        self.gridLayout_3.addWidget(self.copy_resolution, 1, 0, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(parent=self.tab_3)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.gridLayout_3.addWidget(self.comboBox_2, 1, 1, 1, 1)
        self.select_all = QtWidgets.QPushButton(parent=self.tab_3)
        self.select_all.setObjectName("select_all")
        self.gridLayout_3.addWidget(self.select_all, 1, 2, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.image_loader = QtWidgets.QLabel(parent=self.tab_3)
        self.image_loader.setObjectName("image_loader")
        self.verticalLayout_4.addWidget(self.image_loader)
        self.img_name = QtWidgets.QLabel(parent=self.tab_3)
        self.img_name.setObjectName("img_name")
        self.verticalLayout_4.addWidget(self.img_name)
        self.img_size = QtWidgets.QLabel(parent=self.tab_3)
        self.img_size.setObjectName("img_size")
        self.verticalLayout_4.addWidget(self.img_size)
        self.label_4 = QtWidgets.QLabel(parent=self.tab_3)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.copy_selected_btn = QtWidgets.QPushButton(parent=self.tab_3)
        self.copy_selected_btn.setObjectName("copy_selected_btn")
        self.verticalLayout_4.addWidget(self.copy_selected_btn)
        self.gridLayout_4.addLayout(self.verticalLayout_4, 0, 1, 2, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_6 = QtWidgets.QLabel(parent=self.tab_3)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_3.addWidget(self.label_6)
        self.listWidget_5 = ListView_Right(parent=self.tab_3)
        self.listWidget_5.setMinimumSize(QtCore.QSize(0, 500))
        self.listWidget_5.setBaseSize(QtCore.QSize(0, 0))
        self.listWidget_5.setObjectName("listWidget_5")
        self.verticalLayout_3.addWidget(self.listWidget_5)
        self.gridLayout_4.addLayout(self.verticalLayout_3, 0, 2, 2, 1)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.listWidget_3 = ListView_Left(parent=self.tab_3)
        self.listWidget_3.setObjectName("listWidget_3")
        self.verticalLayout_5.addWidget(self.listWidget_3)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtWidgets.QLabel(parent=self.tab_3)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3)
        self.comboBox = QtWidgets.QComboBox(parent=self.tab_3)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.comboBox)
        self.label_8 = QtWidgets.QLabel(parent=self.tab_3)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_8)
        self.clear_selected_btn = QtWidgets.QPushButton(parent=self.tab_3)
        self.clear_selected_btn.setObjectName("clear_selected_btn")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.clear_selected_btn)
        self.verticalLayout_5.addLayout(self.formLayout)
        self.listWidget_4 = ListView_Left(parent=self.tab_3)
        self.listWidget_4.setObjectName("listWidget_4")
        self.verticalLayout_5.addWidget(self.listWidget_4)
        self.gridLayout_4.addLayout(self.verticalLayout_5, 1, 0, 1, 1)
        self.src_code_2.addTab(self.tab_3, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.src_code_2.addTab(self.tab_2, "")
        self.verticalLayout_2.addWidget(self.src_code_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionsettings = QtGui.QAction(parent=MainWindow)
        self.actionsettings.setObjectName("actionsettings")
        self.actionInfo = QtGui.QAction(parent=MainWindow)
        self.actionInfo.setObjectName("actionInfo")

        self.retranslateUi(MainWindow)
        self.src_code_2.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        #other stuff
        self.img_size.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.img_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(7)
        big_font = QFont()
        big_font.setPointSize(15)
        self.listWidget_2.setFont(big_font)
        self.image_loader.setScaledContents(True)
        placeholder_logo = QPixmap("centria.jpg")
        self.image_loader.setPixmap(placeholder_logo)
        self.image_loader.setMaximumSize(QSize(250,250))
        self.image_loader.setMinimumSize(QSize(250,250))
        self.listWidget.setFont(font)
        self.listWidget_3.setFont(font)
        self.label_4.setFont(font)
        self.label_5.setMinimumSize(QSize(30,10))
        self.comboBox.setCurrentIndex(1)
        icon_main = QIcon("16x16/actions/document-preview-archive.png")
        MainWindow.setWindowIcon(icon_main)
        #connections
        self.src_code_search.clicked.connect(self.choose_src_code_directory)
        self.src_code_add_btn.clicked.connect(self.add_name)
        self.icons_folder_btn.clicked.connect(self.choose_icons_directory)
        self.destination_folder_btn.clicked.connect(self.choose_destination_directory)
        self.comboBox.currentIndexChanged.connect(self.loadIcons)
        self.copy_src_code.clicked.connect(self.copyfiles)
        self.search_btn.clicked.connect(self.loadIcons)
        self.copy_resolution.currentIndexChanged.connect(self.loadIcons)
        self.comboBox_2.currentIndexChanged.connect(self.loadIcons)
        self.listWidget_3.clicked.connect(self.on_item_clicked_main)
        self.listWidget_4.clicked.connect(self.delete_item)
        self.listWidget_2.clicked.connect(self.delete_item_src_code)
        self.clear_selected_btn.clicked.connect(self.clear_selected)
        self.select_all.clicked.connect(self.select_all_func)
        self.copy_selected_btn.clicked.connect(self.copy_files)

        self.selected_items = []

        self.toolBar = QtWidgets.QToolBar(parent=MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        button_action = QAction(QIcon("16x16/actions/help-hint.png"), "info", parent=MainWindow)
        button_action.setStatusTip("Readme/info")
        button_action.triggered.connect(self.open_help)
        self.toolBar.addAction(button_action)
        self.toolBar.addSeparator()
        button_action2 = QAction(QIcon("16x16/actions/settings-configure.png"), "settings", parent=MainWindow)
        button_action2.setStatusTip("Settings")
        button_action2.triggered.connect(self.toolBar_settings)
        self.toolBar.addAction(button_action2)

    def toolBar_settings(self, s):
        print("click", s)
    
    def open_help(self):
        popup = QMessageBox()
        popup.setWindowTitle("Info Window")
        long_string = '''
        The idea for this app is to make huge icon sets in to smaller sets.
        1. Choose folder where you have big icon set (icons folder).
        2. Choose folder where to copy all the selected icons (Destination).
        Application then shows all the icons in icons folder where you can filter for different sizes, categories and names.
        You can also give source code in src_code tab to automatically find icons needed.
        src code search made for Qt projects.
        More options coming later
        '''
        popup.setText(long_string)
        popup.exec()

    def showLoadingSpinner(self, visible):
        spinner_path = "spinner_smaller.gif"
        movie = QMovie(spinner_path)
        self.label_5.setMovie(movie)

        if visible:
            movie.start()
            self.label_5.show()
        else:
            movie.stop()
            self.label_5.hide()

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
            #self.label_4.setText(data)
        except Exception as e:
            print("An error occurred: " + str(e))

    def clear_selected(self):
        self.listWidget_4.m_model.clear()

    def delete_item(self, item):
        row = item.row()
        self.listWidget_4.m_model.removeRow(row)

    def delete_item_src_code(self, item):
        row = item.row()
        index = self.listWidget_2.itemFromIndex(item)
        name = index.text()
        self.listWidget_2.takeItem(row)
        if name in names_to_match:
            names_to_match.remove(name)

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
            if index >= 200:
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
            if index >= 200:
                break
            item = QStandardItem()
            item.setIcon(QIcon(icon))
            file_name = os.path.basename(icon)
            split_name = file_name.split(".")[0]
            item.setText(split_name)
            self.listWidget_5.m_model.appendRow(item)

    def loadIcons(self):
        search_term = self.search_text.input_field.text()
        folder_path = self.icons_folder.text()
        resolution_check = self.copy_resolution.currentText()
        categories_check = self.comboBox_2.currentText()
        if resolution_check == "None":
            resolution_check = None
        if categories_check == "None":
            categories_check = None
        if len(folder_path) > 2:
            if not os.path.exists(folder_path):
                return
            number = int(self.comboBox.currentText())
            worker = LoadIconsWorker(folder_path, search_term, resolution_check, number,categories_check, self)
            QThreadPool.globalInstance().start(worker)

    def load_boxes(self, path):
            items = get_all_resolutions(path)
            for item in items:
                self.copy_resolution.addItem(item)
                checkbox = QCheckBox(item)
                checkbox.stateChanged.connect(lambda state, cb=checkbox: self.checkbox_state_changed(state, cb))
                self.gridLayout_2.addWidget(checkbox)
    
    def choose_icons_directory(self):
        dir_name = QFileDialog.getExistingDirectory(self.centralwidget, "Select a Directory")
        if dir_name:
            path = Path(dir_name)
            self.icons_folder.setText(str(path))
            self.load_boxes(self.icons_folder.text())
            self.loadIcons()

    def checkbox_state_changed(self, state, checkbox):
        item = checkbox.text()
        if not item in self.selected_items:
            self.selected_items.append(item)
        else:
            self.selected_items.remove(item)

    def choose_destination_directory(self):
        dir_name = QFileDialog.getExistingDirectory(self.centralwidget, "Select a Directory")
        if dir_name:
            path = Path(dir_name)
            self.destination_folder.setText(str(path))
            self.loadIcons_dest(path)
            self.loadIcons_dest2(path)


    def choose_src_code_directory(self):
        self.listWidget_2.clear()
        dir_name = QFileDialog.getExistingDirectory(self.centralwidget, "Select a Directory")
        if dir_name:
            path = Path(dir_name)
            self.src_code_folder.setText(str(path))
            find_icons_in_files(dir_name)
            for icon in names_to_match:
                self.listWidget_2.addItem(icon)
                
    def add_name(self):
        name = self.src_code_add.input_field.text()
        if name:
            names_to_match.append(name)
            self.listWidget_2.addItem(name)
            self.src_code_add.input_field.clear()

    def copyfiles(self):
        source_folder = self.icons_folder.text()
        destination_folder = self.destination_folder.text()
        svg_files = get_svg_files(source_folder) 
        index_themes = get_themes(source_folder)  
        src_code = self.src_code_folder.text()
        check_all_found = names_to_match
        find_icons_in_files(src_code)
        resolution_check = self.selected_items
        if not resolution_check:
            resolution_check = None
        try:
            if not os.path.exists(source_folder):
                dlg = QMessageBox()
                dlg.setWindowTitle("error")
                dlg.setText("invalid icon src path")
                dlg.exec()
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
                    if resolution_check:
                        icon_resolution = get_icon_resolution(file)
                        if icon_resolution in resolution_check:
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

            self.loadIcons_dest(destination_folder)
            self.loadIcons_dest2(destination_folder)
            
            if len(check_all_found) > 0:
                arr = []
                print("files not found:")
                for file in check_all_found:
                    arr.append(file)
                combinedString = ','.join(arr)
                whole_message = "Icons not found: " + combinedString
                dlg = QMessageBox()
                dlg.setWindowTitle("error")
                dlg.setText(whole_message)
                dlg.exec()
            else:
                dlg = QMessageBox()
                dlg.setWindowTitle("copied icons")
                dlg.setText("Found all icons needed!")
                dlg.exec()
        except Exception as e:
            print("An error occurred: " + str(e))

    def copy_files(self):
        source_folder = self.icons_folder.text()
        destination_folder = self.destination_folder.text()
        index_themes = get_themes(source_folder) 
        try:
            if not os.path.exists(source_folder):
                dlg = QMessageBox()
                dlg.setWindowTitle("error")
                dlg.setText("invalid icon src path")
                dlg.exec()
                return
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            for file in index_themes:
                relative_path = os.path.relpath(file, source_folder)
                destination_subfolder = os.path.dirname(os.path.join(destination_folder, relative_path))
                os.makedirs(destination_subfolder, exist_ok=True)

                destination_path = os.path.join(destination_subfolder, os.path.basename(file))
                if not os.path.exists(destination_path):
                    shutil.copy(file, destination_path)

            for row in range(self.listWidget_4.m_model.rowCount()):
                index = self.listWidget_4.m_model.index(row,0)
                item = self.listWidget_4.m_model.itemFromIndex(index)
                data = item.data()
                # Get the relative path of the source file
                relative_path = os.path.relpath(data, source_folder)
                destination_subfolder = os.path.dirname(os.path.join(destination_folder, relative_path))
                os.makedirs(destination_subfolder, exist_ok=True)
                destination_path2 = os.path.join(destination_subfolder, os.path.basename(data))
                if os.path.exists(destination_path2):
                    print(f"File '{os.path.basename(data)}' already exists in the destination folder.")
                else:
                    shutil.copy(data, destination_path2)
            self.listWidget_4.m_model.clear()
            self.loadIcons_dest(destination_folder)
            self.loadIcons_dest2(destination_folder)
            dlg = QMessageBox()
            dlg.setWindowTitle("copied icons!")
            dlg.setText("Succesfully copied icons!")
            dlg.exec()
           # button = dlg.exec()
           # if button == QMessageBox.StandardButton.Ok:
           #     print("OK!")
        except Exception as e:
            print("An error occurred: " + str(e))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Icon compiler"))
        self.icons_folder_btn.setText(_translate("MainWindow", "Icons folder"))
        self.label_5.setText(_translate("MainWindow", ""))
        self.destination_folder_btn.setText(_translate("MainWindow", "Destination"))
        self.src_code_2.setToolTip(_translate("MainWindow", "<html><head/><body><p>src code</p></body></html>"))
        self.src_code_2.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>src code</p><p><br/></p></body></html>"))
        self.src_code_search.setText(_translate("MainWindow", "src code"))
        self.label.setText(_translate("MainWindow", "Found icon names:"))
        self.src_code_add_btn.setText(_translate("MainWindow", "add icon"))

        self.copy_src_code.setText(_translate("MainWindow", "Copy icons"))
        self.label_2.setText(_translate("MainWindow", "Icons in destination folder"))
        self.src_code_2.setTabText(self.src_code_2.indexOf(self.src_code), _translate("MainWindow", "src_code"))
        self.search_btn.setText(_translate("MainWindow", "Search"))
        self.search_btn.setShortcut(_translate("MainWindow", "Return"))
        self.copy_resolution.setItemText(0, _translate("MainWindow", "None"))
        self.select_all.setText(_translate("MainWindow", "Select all"))
        self.image_loader.setText(_translate("MainWindow", "\"Img\""))
        self.img_name.setText(_translate("MainWindow", ""))
        self.img_size.setText(_translate("MainWindow", ""))
        self.label_4.setText(_translate("MainWindow", ""))
        self.copy_selected_btn.setText(_translate("MainWindow", "Copy selected"))
        self.label_6.setText(_translate("MainWindow", "Icons in destination folder:"))
        self.label_3.setText(_translate("MainWindow", "Icons loaded"))
        self.comboBox.setItemText(0, _translate("MainWindow", "10"))
        self.comboBox.setItemText(1, _translate("MainWindow", "25"))
        self.comboBox.setItemText(2, _translate("MainWindow", "50"))
        self.comboBox.setItemText(3, _translate("MainWindow", "100"))
        self.comboBox.setItemText(4, _translate("MainWindow", "200"))
        self.comboBox.setItemText(5, _translate("MainWindow", "500"))
        self.comboBox.setItemText(6, _translate("MainWindow", "1000"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "None"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "actions"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "apps"))
        self.comboBox_2.setItemText(3, _translate("MainWindow", "emotes"))
        self.comboBox_2.setItemText(4, _translate("MainWindow", "devices"))
        self.comboBox_2.setItemText(5, _translate("MainWindow", "categories"))
        self.comboBox_2.setItemText(6, _translate("MainWindow", "status"))

        self.label_8.setText(_translate("MainWindow", "selected icons"))
        self.clear_selected_btn.setText(_translate("MainWindow", "Clear"))
        self.src_code_2.setTabText(self.src_code_2.indexOf(self.tab_3), _translate("MainWindow", "copy"))
        self.src_code_2.setTabText(self.src_code_2.indexOf(self.tab_2), _translate("MainWindow", "theme gen"))
        self.actionsettings.setText(_translate("MainWindow", "settings"))
        self.actionInfo.setText(_translate("MainWindow", "Info/help"))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()