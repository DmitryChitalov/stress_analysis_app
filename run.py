#!/usr/bin/python3
# -*- coding: utf-8 -*-
###-------------------------------Импорт модулей----------------------------------###

import sys
import os
from PyQt5 import QtCore
from PyQt5 import QtSql
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QRadioButton, QGridLayout, \
    QLineEdit, QPushButton, QHBoxLayout, QFrame, QVBoxLayout, QFormLayout, \
    QFileDialog, QListWidgetItem, QTableView, QApplication, QMainWindow, QAction, \
    QDockWidget, QGridLayout, QFrame, QScrollArea, QListWidget, QApplication, \
    QStyle, QToolBar, QTextEdit, QTreeView, QListWidgetItem

from add_classes.file_form_class import file_form_class

from functions.first_toolbar_functions import first_toolbar_functions_class
from functions.second_toolbar_functions import second_toolbar_functions_class

from threads.msh_threads import msh_generation_thread

###-------------------------Главное окно программы-----------------------------###

class MainWindowClass(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.interface_lng_val = 'Russian'
        self.setWindowTitle("Графический интерфейс программы OpenFOAM")

        self.full_dir = ''
        self.prj_name = ''
        self.con = ''

        # ---------------------------Панель управления решением задачи МСС----------------------------- #

        self.proj_open = QAction(self)
        self.proj_open.setEnabled(True)
        proj_ico = self.style().standardIcon(QStyle.SP_ArrowUp)
        self.proj_open.setIcon(proj_ico)
        self.proj_open.setToolTip('Открыть проект')

        self.lng_chs = QAction(self)
        self.lng_chs.setEnabled(True)
        lng_chs_ico = self.style().standardIcon(QStyle.SP_FileDialogDetailedView)
        self.lng_chs.setIcon(lng_chs_ico)
        self.lng_chs.setToolTip('Выбрать язык интерфейса программы')

        self.toolBar_1 = QToolBar("MyToolBar")
        self.toolBar_1.addAction(self.proj_open)
        self.toolBar_1.addAction(self.lng_chs)

        self.proj_open.triggered.connect(lambda: first_toolbar_functions_class.on_proj_open(self))

        self.addToolBar(self.toolBar_1)
		
        ###----------------------Панель управления подготовкой РС--------------------------###

        self.msh_open = QAction(self)
        self.msh_open.setEnabled(False)
        msh_ico = self.style().standardIcon(QStyle.SP_FileDialogNewFolder)
        self.msh_open.setIcon(msh_ico)
        self.msh_open.setToolTip('Открыть форму выбора расчетной сетки')

        self.msh_run = QAction(self)
        self.msh_run.setEnabled(False)
        msh_ico = self.style().standardIcon(QStyle.SP_ArrowRight)
        self.msh_run.setIcon(msh_ico)
        self.msh_run.setToolTip('Выполнить генерацию расчетной сетки')

        self.msh_visual = QAction(self)
        self.msh_visual.setEnabled(False)
        msh_visual_ico = self.style().standardIcon(QStyle.SP_MediaSeekForward)
        self.msh_visual.setIcon(msh_visual_ico)
        self.msh_visual.setToolTip('Выполнить визуализацию расчетной сетки')

        self.toolBar_2 = QToolBar()
        self.toolBar_2.addAction(self.msh_open)
        self.toolBar_2.addAction(self.msh_run)
        self.toolBar_2.addAction(self.msh_visual)

        self.msh_open.triggered.connect(lambda: second_toolbar_functions_class.on_msh_open(self))
        self.msh_run.triggered.connect(lambda: second_toolbar_functions_class.on_msh_run(prj_path_val, mesh_name_txt_val, pp_dir, self, self.interface_lng_val, msh_type))

        self.msh_visual.triggered.connect(lambda: second_toolbar_functions_class.on_visual_msh_run(prj_path_val, mesh_name_txt_val, pp_dir, self, self.interface_lng_val, msh_type))
        
        self.addToolBar(self.toolBar_2)
        self.insertToolBarBreak(self.toolBar_2)

        ###----------------------Панель управления проведением стресс-анализа--------------------------###

        self.str_an_run = QAction(self)
        self.str_an_run.setEnabled(False)
        str_an_ico = self.style().standardIcon(QStyle.SP_CommandLink)
        self.str_an_run.setIcon(str_an_ico)
        self.str_an_run.setToolTip('Выполнить стресс-анализ')

        self.str_an_vis_run = QAction(self)
        self.str_an_vis_run.setEnabled(False)
        str_an_vis_ico = self.style().standardIcon(QStyle.SP_MediaPlay)
        self.str_an_vis_run.setIcon(str_an_vis_ico)
        self.str_an_vis_run.setToolTip('Выполнить визуализацию результатов стресс-анализ')

        self.toolBar_3 = QToolBar()
        self.toolBar_3.addAction(self.str_an_run)
        self.toolBar_3.addAction(self.str_an_vis_run)

        self.str_an_run.triggered.connect(
            lambda: second_toolbar_functions_class.on_str_an_run(prj_path_val, mesh_name_txt_val, pp_dir, self, self.interface_lng_val, msh_type))

        self.str_an_vis_run.triggered.connect(
            lambda: second_toolbar_functions_class.on_visual_on_str_an_run(prj_path_val, mesh_name_txt_val, pp_dir, self, self.interface_lng_val, msh_type))

        self.addToolBar(self.toolBar_3)
        self.insertToolBarBreak(self.toolBar_3)
                        
        ###----------------Верхний виджет с полным путем до файла сетки----------------###

        self.tdw = QDockWidget()
        self.tdw.setFixedSize(1400, 65)
        self.tdw.setFeatures(self.tdw.NoDockWidgetFeatures)       
        self.tdw_grid = QGridLayout()
        self.tdw_grid.setColumnStretch(2, 1)
        self.tdw_frame = QFrame()
        self.tdw_frame.setStyleSheet("background-color: ghostwhite;" "border-width: 0.5px;" "border-style: solid;" "border-color: silver;")
        self.tdw_frame.setLayout(self.tdw_grid)
        self.tdw.setWidget(self.tdw_frame)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, self.tdw)

        ###-----------------Левый виджет с файловой системой проекта---------------------###

        self.fsw = QDockWidget()
        self.fsw.setFeatures(self.fsw.NoDockWidgetFeatures)
        self.fsw_label = QLabel()
        self.fsw_label.setAlignment(QtCore.Qt.AlignCenter)
        self.fsw_grid = QGridLayout()
        self.fsw_grid.addWidget(self.fsw_label, 0, 0)
        self.fsw_frame = QFrame()
        self.fsw_frame.setFixedSize(200, 35)
        self.fsw_frame.setStyleSheet(
            "background-color: honeydew;" "border-width: 1px;" "border-style: solid;" "border-color: dimgray;" "border-radius: 4px;")
        self.fsw_frame.setLayout(self.fsw_grid)
        fs_lbl = "Файловая структура проекта"
        self.fsw_label.setText("<font color='SeaGreen'>" + fs_lbl + "</font>")
        self.fsw_label.setStyleSheet("border-style: none;" "font-size: 10pt;")
        self.fsw.setTitleBarWidget(self.fsw_frame)
        self.treeview = QTreeView()
        self.treeview.setFixedSize(200, 520)
        self.treeview.model = QtGui.QStandardItemModel()
        self.treeview.setModel(self.treeview.model)
        self.treeview.setColumnWidth(0, 100)
        self.treeview.setColumnHidden(1, True)
        self.treeview.setColumnHidden(2, True)
        self.treeview.setColumnHidden(3, True)
        self.treeview.header().hide()
        self.treeview.setItemsExpandable(False)
        self.treeview.clicked.connect(self.on_treeview_clicked)
        self.fsw.setWidget(self.treeview)

        ###-----------Правый виджет с формой вывода результатов генерации файлов-----------###

        self.cdw = QDockWidget()
        self.cdw.setFeatures(self.cdw.NoDockWidgetFeatures)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.cdw)

        self.cdw_grid = QGridLayout()
        self.cdw_frame = QFrame()
        self.cdw_frame.setFixedSize(495, 35)
        self.cdw_frame.setStyleSheet(
            "border-width: 1px;" "border-style: solid;" "border-color: dimgray;" "border-radius: 4px;" "background-color: honeydew;")
        self.cdw_frame.setLayout(self.cdw_grid)

        self.outf_lbl = QLabel()
        self.outf_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.outf_lbl.setStyleSheet("border-style: none;" "font-size: 9pt;")

        self.cdw_grid.addWidget(self.outf_lbl, 0, 0)

        self.outf_edit = QTextEdit()
        self.outf_scroll = QScrollArea()
        self.outf_scroll.setWidgetResizable(True)
        self.outf_scroll.setWidget(self.outf_edit)
        self.outf_scroll.setFixedSize(495, 520)

        ###-----------------Центральный виджет с формой параметров---------------------###

        self.ffw = QDockWidget()
        self.ffw.setFeatures(self.ffw.NoDockWidgetFeatures)
        self.ffw_label = QLabel()
        self.ffw_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ffw_grid = QGridLayout()
        self.ffw_grid.addWidget(self.ffw_label, 0, 0)
        self.ffw_frame = QFrame()
        self.ffw_frame.setFixedSize(693, 44)
        self.ffw_frame.setStyleSheet(
            "border-width: 1px;" "border-style: solid;" "border-color: dimgray;" "border-radius: 4px;" "background-color: honeydew;")
        self.ffw_frame.setLayout(self.ffw_grid)

        ###------------------Нижний виджет со служебными сообщениями------------------###

        self.serv_mes = QDockWidget("Служебные сообщения")
        self.serv_mes.setFixedSize(1400, 160)
        self.serv_mes.setFeatures(self.serv_mes.NoDockWidgetFeatures)
        self.listWidget = QListWidget()
        self.serv_mes.setWidget(self.listWidget)

    ###---------------------Функции, связанные с работой главного окна------------------------###

    # ...........................Функция клика по файлу из дерева.........................

    ###........................Функция открытия окна выбора интерфейса программы...................###         

    # ...........................Функция клика по файлу из дерева.........................

    def on_treeview_clicked(self, index):
        global fileName
        indexItem = self.treeview.model.index(index.row(), 0, index.parent())
        file_name = self.treeview.model.itemFromIndex(indexItem).text()
        file_form_class.inp_file_form_func(self, file_name, self.con)
        file_name_title = file_form_class.out_file_name_func()
        self.clear_label = QLabel()
        if file_name_title != None:
            self.cdw.setWidget(self.clear_label)
            self.cdw.setTitleBarWidget(self.clear_label)
            self.setCentralWidget(self.ffw)
            file_form = file_form_class.out_file_form_func()
            self.ffw.setWidget(file_form)
            self.ffw.setTitleBarWidget(self.ffw_frame)
            self.ffw_label.setText("Форма параметров файла: " + "<font color='peru'>" + file_name_title + "</font>")
            self.ffw_label.setStyleSheet("border-style: none;" "font-size: 9pt;")
        else:

            self.ffw.setTitleBarWidget(self.clear_label)
            self.ffw.setWidget(self.clear_label)
            self.cdw.setWidget(self.clear_label)
            self.cdw.setTitleBarWidget(self.clear_label)

        if file_name_title == 'blockMeshDict' or file_name_title == 'snappyHexMeshDict':
            if self.interface_lng_val == 'Russian':
                msg_lbl = QLabel(
                    '<span style="color:blue">Для создания расчетной сетки воспользуйтесь панелью инструментов</span>')
            elif self.interface_lng_val == 'English':
                msg_lbl = QLabel(
                    '<span style="color:blue">For computational mesh generation use the toolbar</span>')

            self.listWidget.clear()
            self.item = QListWidgetItem()
            self.listWidget.addItem(self.item)
            self.listWidget.setItemWidget(self.item, msg_lbl)

    # .........................Функция получения языка интерфейса..........................

    def on_lng_get(self, interface_lng):
        global interface_lng_val

        self.interface_lng_val = interface_lng

        if self.interface_lng_val == 'Russian':
            self.setWindowTitle("Генератор расчетных сеток")
            self.prj_open.setToolTip('Открыть проект')
            self.msh_run.setToolTip('Выполнить генерацию расчетной сетки')
            self.msh_visual.setToolTip('Выполнить визуализацию расчетной сетки')
            self.lng_chs.setToolTip('Выбрать язык интерфейса программы')
        elif self.interface_lng_val == 'English':
            self.setWindowTitle("Mesh generator")
            self.prj_open.setToolTip('Open project')
            self.msh_run.setToolTip('Run mesh generation')
            self.msh_visual.setToolTip('Run mesh vizualization')
            self.lng_chs.setToolTip('Select the interface language for the program')

    # .........................Функция получения пути до директории..........................

    def on_prj_path_get(self, prj_path, mesh_name_txt):
        global prj_path_val
        global mesh_name_txt_val
        global pp_dir

        prj_path_val = prj_path
        mesh_name_txt_val = mesh_name_txt

        pp_dir, pp_sys = os.path.split(prj_path_val)

    # .............................Функция получения типа сетки..............................

    def on_mesh_type_get(self, pd_2):
        global msh_type
        msh_type = pd_2

    #def on_msg_correct(self, msg):
        #self.listWidget.clear()
        #self.item = QListWidgetItem(msg, self.listWidget)
        #color = QtGui.QColor("green")
        #self.item.setTextColor(color)
        #self.listWidget.addItem(self.item)

    #def on_msg_error(self, msg_list):
        #self.listWidget.clear()
        #for msg in msg_list:
            #self.item = QListWidgetItem(msg, self.listWidget)
            #self.listWidget.addItem(self.item)
			
    



###---------------------------Формирование главного окна программы-------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindowClass()
    window.setFixedSize(1400, 900)
    window.setGeometry(200, 30, 0, 0)
    window.show()
    sys.exit(app.exec_())
       
