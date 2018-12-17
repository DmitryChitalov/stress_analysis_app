# -*- coding: utf-8 -*-
# -------------------------------Импорт модулей----------------------------------#

from PyQt5 import QtCore
from PyQt5 import QtSql
from PyQt5 import QtGui

from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QRadioButton, QGridLayout, QFrame, QLineEdit, QVBoxLayout, QListWidgetItem, QPushButton, QStyle, QFormLayout, QFileDialog, QMessageBox

import shutil
import sys
import re
import os
import os.path
import subprocess
import time
import getpass

from windows.bMD_window import bmd_window_class
from windows.sHMD_window import shmd_window_class

# -----------Дочерний поток для запуска процесса генерации сетки-----------------

class MyThread(QtCore.QThread):
    def __init__(self, full_dir, parent=None):
        QtCore.QThread.__init__(self, parent)
        global fd
        fd = full_dir
    def run(self):
        global proc

        file = open(fd+"/out_mesh.log", "w")
        proc = subprocess.Popen(["bash "+fd+"/MESH_BASH"], cwd = fd, shell = True, stdout=file, stderr=file)
        while proc.poll() is None:
            time.sleep(0.5)

# ---------------------------Главная форма проекта-------------------------------#
		
class msh_window_class(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowSystemMenuHint)
		self.setWindowModality(QtCore.Qt.WindowModal)

		global par
		par = parent
		
		global int_lng
		int_lng = par.interface_lng_val	
		
		global full_dir
		full_dir = parent.full_dir
		self.t1 = MyThread(full_dir)
		
# ------------------------------------Первый блок формы--------------------------------------#

		self.mesh_choose_lbl = QLabel()
		self.mesh_choose_lbl_hbox = QHBoxLayout()
		self.mesh_choose_lbl_hbox.addWidget(self.mesh_choose_lbl)
		self.radio_1 = QRadioButton()
		self.radio_1.toggled.connect(self.on_radio_1_clicked)
		self.radio_2 = QRadioButton()
		self.radio_2.toggled.connect(self.on_radio_2_clicked)
		self.mesh_choose_grid = QGridLayout()
		self.mesh_choose_grid.addWidget(self.radio_1, 0, 0)
		self.mesh_choose_grid.addWidget(self.radio_2, 0, 1)
		self.mesh_choose_frame = QFrame()
		self.mesh_choose_frame.setLayout(self.mesh_choose_grid)
		self.mesh_choose_hbox = QHBoxLayout() 
		self.mesh_choose_hbox.addWidget(self.mesh_choose_frame)
		
# ------------------------------------Второй блок формы--------------------------------------#

		self.fmtf_radio = QRadioButton("Импорт 2D-сетки")
		self.f3Dmtf_radio = QRadioButton("Импорт 3D-сетки")
		self.import_hbox = QHBoxLayout()
		self.import_hbox.addWidget(self.fmtf_radio)
		self.import_hbox.addWidget(self.f3Dmtf_radio)
		
		self.mesh_label = QLabel("Путь: ")
		self.mesh_edit = QLineEdit()
		self.mesh_edit.setEnabled(False)
		self.mesh_edit.setFixedSize(290, 25)
		self.path_button = QPushButton("...")
		self.path_button.setFixedSize(25, 25)
		
		self.import_prs_hbox = QHBoxLayout()
		self.import_prs_hbox.addWidget(self.mesh_label)
		self.import_prs_hbox.addWidget(self.mesh_edit)
		self.import_prs_hbox.addWidget(self.path_button)
		self.path_button.clicked.connect(self.on_path_choose)

		self.prs_grid = QGridLayout()
		self.prs_grid.addLayout(self.import_hbox, 0, 0)
		self.prs_grid.addLayout(self.import_prs_hbox, 1, 0)
		self.prs_frame = QFrame()
		self.prs_frame.setStyleSheet(open("./styles/properties_form_style.qss","r").read())
		self.prs_frame.setLayout(self.prs_grid)
		self.prs_frame.setEnabled(False)
		self.prs_frame.setStyleSheet("border-color: darkgray;")
		self.prs_hbox = QHBoxLayout() 
		self.prs_hbox.addWidget(self.prs_frame)

		# ------------------------------------Третий блок формы--------------------------------------#

		self.chc_label = QLabel()
		self.chc_label.setEnabled(False)
		self.chc_lbl_hbox = QHBoxLayout()
		self.chc_lbl_hbox.addWidget(self.chc_label)
		self.nf_radio = QRadioButton()
		self.nf_radio.toggled.connect(self.on_nf_clicked)
		self.cf_radio = QRadioButton()
		self.cf_radio.toggled.connect(self.on_cf_clicked)
		self.icon = self.style().standardIcon(QStyle.SP_DirOpenIcon)
		self.chc_button = QPushButton()
		self.chc_button.setFixedSize(30, 30)
		self.chc_button.setIcon(self.icon)
		self.chc_button.setEnabled(False)
		self.chc_button.clicked.connect(self.on_chc_clicked)
		self.chc_grid = QGridLayout()
		self.chc_grid.addWidget(self.nf_radio, 0, 0)
		self.chc_grid.addWidget(self.cf_radio, 0, 1)
		self.chc_grid.addWidget(self.chc_button, 0, 2)
		self.chc_frame = QFrame()
		self.chc_frame.setFixedWidth(400)
		self.chc_frame.setEnabled(False)
		self.chc_frame.setStyleSheet("border-color: darkgray;")
		self.chc_frame.setLayout(self.chc_grid)
		self.chc_hbox = QHBoxLayout() 
		self.chc_hbox.addWidget(self.chc_frame)
		
		# ------------------------------------Четвертый блок формы--------------------------------------#

		self.mesh_type_label = QLabel('Выберите тип сетки:')
		self.bm = QRadioButton("blockMesh")
		self.bm.setChecked(True)
		self.shm = QRadioButton("snappyHexMesh")
		self.mesh_type_vbox = QVBoxLayout()
		self.mesh_type_vbox.addWidget(self.bm)
		self.mesh_type_vbox.addWidget(self.shm)
		
		self.mesh_label = QLabel()
		self.mesh_name = QLineEdit()
		
		self.mesh_name.setFixedSize(214, 25)
		regexp = QtCore.QRegExp('[А-яА-Яa-zA-Z0-9\_]+')
		validator = QtGui.QRegExpValidator(regexp)
		self.mesh_name.setValidator(validator)
		
		self.prj_path_label = QLabel()
		self.prj_path_name = QLineEdit()
		self.prj_path_name.setEnabled(False)
		self.prj_path_name.setFixedSize(214, 25)
				
		self.prj_grid = QGridLayout()
		self.prj_grid.addWidget(self.mesh_type_label, 0, 0, alignment=QtCore.Qt.AlignCenter)
		self.prj_grid.addLayout(self.mesh_type_vbox, 0, 1, alignment=QtCore.Qt.AlignCenter)
		self.prj_grid.addWidget(self.mesh_label, 1, 0, alignment=QtCore.Qt.AlignCenter)
		self.prj_grid.addWidget(self.mesh_name, 1, 1, alignment=QtCore.Qt.AlignCenter)
		self.prj_grid.addWidget(self.prj_path_label, 2, 0, alignment=QtCore.Qt.AlignCenter)
		self.prj_grid.addWidget(self.prj_path_name, 2, 1, alignment=QtCore.Qt.AlignCenter)

		self.prj_frame = QFrame()
		self.prj_frame.setFixedWidth(400)
		self.prj_frame.setEnabled(False)
		self.prj_frame.setStyleSheet("border-color: darkgray;")
		self.prj_frame.setFrameShape(QFrame.Panel)
		self.prj_frame.setFrameShadow(QFrame.Sunken)
		self.prj_frame.setLayout(self.prj_grid) 
		self.prj_grid_vbox = QVBoxLayout() 
		self.prj_grid_vbox.addWidget(self.prj_frame)

		# ---------------------Кнопки сохранения и отмены и их блок-------------------------#

		self.save_button = QPushButton()
		self.save_button.setFixedSize(80, 25)
		self.save_button.clicked.connect(self.on_save_clicked)
		self.save_button.setEnabled(False)
		self.cancel_button = QPushButton()
		self.cancel_button.setFixedSize(80, 25)
		self.cancel_button.clicked.connect(self.on_cancel_clicked)
		self.buttons_hbox = QHBoxLayout()
		self.buttons_hbox.addWidget(self.save_button)
		self.buttons_hbox.addWidget(self.cancel_button)

		# -------------------------Фрейм формы---------------------------#

		self.form_grid = QGridLayout()
		self.form_grid.addLayout(self.mesh_choose_hbox, 0, 0, alignment=QtCore.Qt.AlignCenter)
		self.form_grid.addLayout(self.prs_hbox, 1, 0, alignment=QtCore.Qt.AlignCenter)
		self.form_grid.addLayout(self.chc_lbl_hbox, 2, 0, alignment=QtCore.Qt.AlignCenter)
		self.form_grid.addLayout(self.chc_hbox, 3, 0, alignment=QtCore.Qt.AlignCenter)
		self.form_grid.addLayout(self.prj_grid_vbox, 4, 0, alignment=QtCore.Qt.AlignCenter)
		self.form_grid.addLayout(self.buttons_hbox, 5, 0, alignment=QtCore.Qt.AlignCenter)
		self.form_frame = QFrame()
		self.form_frame.setStyleSheet(open("./styles/properties_form_style.qss","r").read())
		self.form_frame.setLayout(self.form_grid)
		self.form_vbox = QVBoxLayout() 
		self.form_vbox.addWidget(self.form_frame)

		# --------------------Размещение на форме всех компонентов---------#

		self.form = QFormLayout()
		self.form.addRow(self.form_vbox)
		self.setLayout(self.form)
		
		# --------------------Определяем параметры интерфейса окна---------#
		
		if int_lng == 'Russian':
			self.radio_1.setText("Внешняя сетка")
			self.radio_2.setText("OpenFOAM-сетка")
			self.fmtf_radio.setText("Импорт 2D-сетки")
			self.f3Dmtf_radio.setText("Импорт 3D-сетки")
			self.chc_label.setText("Создайте новую сетку или откройте существующую")
			self.nf_radio.setText("Создать новую")
			self.cf_radio.setText("Открыть существующую")
			self.mesh_type_label.setText("Выберите тип сетки:")
			self.mesh_label.setText("Название сетки:")
			self.prj_path_label.setText("Путь:")
			self.save_button.setText("Сохранить")
			self.cancel_button.setText("Отмена")
		elif int_lng == 'English':
			self.radio_1.setText("External mesh")
			self.radio_2.setText("OpenFOAM-mesh")
			self.fmtf_radio.setText("2D-mesh import")
			self.f3Dmtf_radio.setText("3D-mesh import")
			self.chc_label.setText("Create a new mesh or open an existing mesh")
			self.nf_radio.setText("Create new mesh")
			self.cf_radio.setText("Open existing mesh")
			self.mesh_type_label.setText("Select mesh type:")
			self.mesh_label.setText("Mesh name:")
			self.prj_path_label.setText("Path:")
			self.save_button.setText("Save")
			self.cancel_button.setText("Cancel")
		
	# ------------------------Функции связанные с формой-----------------------------#
	
	# .....Функция, запускаемая при нажатии радио-кнопки "Внешняя сетка"......#
	
	def on_radio_1_clicked(self):
		self.prs_frame.setEnabled(True)
		self.chc_frame.setEnabled(False)
		self.prj_frame.setEnabled(False)
		self.chc_label.setEnabled(False)
		self.prs_frame.setStyleSheet("border-color: dimgray;")
		self.chc_frame.setStyleSheet("border-color: darkgray;")
		self.prj_frame.setStyleSheet("border-color: darkgray;")
		self.prj_path_name.setText("")
		
	# .....Функция, запускаемая при нажатии радио-кнопки "OpenFOAM сетка"......#
		
	def on_radio_2_clicked(self):
		self.prs_frame.setEnabled(False)
		self.chc_frame.setEnabled(True)
		self.chc_label.setEnabled(True)
		self.chc_frame.setStyleSheet("border-color: dimgray;")
		self.prs_frame.setStyleSheet("border-color: darkgray;")
		self.prj_path_name.setText(full_dir + '/system')
		self.save_button.setEnabled(True)
	
	# .....Функция определения пути до внешней сетки......#
	
	def on_path_choose(self):
		global mesh_dir
		user = getpass.getuser()
		mesh_dir = QFileDialog.getOpenFileName(directory="/home/"+user)
		mesh_reg = re.compile(r"\S*(?<=[\/])\S*msh")
		mesh_mas = mesh_reg.findall(mesh_dir)

		if mesh_mas != []:
			self.mesh_edit.setText(mesh_dir)
		else:
			dialog = QMessageBox(QMessageBox.Critical,
				"Внимание!", "Это не файл сетки. Выберите другой файл",
				buttons = QMessageBox.Ok)
			result = dialog.exec_()
			
		self.save_button.setEnabled(True)
		
    #......Функция по завершению генерации внешней сетки......#
	
	def on_finished(self):
		global mas

		if proc.returncode == 0:

			file = open(full_dir+"/constant/polyMesh/boundary", 'r') 
			data = file.read()
			file.close()

			struct_reg = re.compile(r"\S*\n\s*(?=[{])")
			struct_mas = struct_reg.findall(data)

			i = 1
			mas = []
			for elem in range(len(struct_mas)-1):
				div = struct_mas[i].split("\n")
				i = i + 1
				mas.append(div[0])

			file_U = open(full_dir+"/0/U", 'a')                 
			file_U.write("\n{\n")
			for el in range(len(mas)):
				file_U.write("    " + mas[el] + "\n    {\n        type            empty;\n    }\n")
			file_U.write("}")
			file_U.close()

			file_T = open(full_dir+"/0/T", 'a')                 
			file_T.write("\n{\n")
			for el in range(len(mas)):
				file_T.write("    " + mas[el] + "\n    {\n        type            empty;\n    }\n")
			file_T.write("}")
			file_T.close()

			file_p = open(full_dir+"/0/p", 'a')                 
			file_p.write("\n{\n")
			for el in range(len(mas)):
				file_p.write("    " + mas[el] + "\n    {\n        type            empty;\n    }\n")
			file_p.write("}")
			file_p.close()

			par.listWidget.clear()
			par.item = QListWidgetItem("Расчетная сетка успешно сгенерирована", par.listWidget)
			par.color = QtGui.QColor("green")
			par.item.setTextColor(par.color)
			par.listWidget.addItem(par.item)
			
			par.task_open.setEnabled(True)
		
			self.close()
		else:
			par.item = QListWidgetItem("Расчетная сетка не сгенерирована", par.listWidget)
			par.color = QtGui.QColor("red")
			par.item.setTextColor(par.color)
			par.listWidget.addItem(par.item)
		
	# .....Функция, запускаемая при нажатии радио-кнопки "создать новую сетку OpenFOAM"......#
	
	def on_nf_clicked(self):
		self.prj_path_label.setEnabled(True)
		self.prj_frame.setEnabled(True)
		self.prj_frame.setStyleSheet("border-color: dimgray;")
		self.chc_button.setEnabled(False)

	# .....Функция, запускаемая при нажатии радио-кнопки "открыть имеющуюся сетку OpenFOAM"......#

	def on_cf_clicked(self):
		self.prj_path_label.setEnabled(False)
		self.prj_frame.setEnabled(False)
		self.prj_frame.setStyleSheet("border-color: darkgray;")
		self.chc_button.setEnabled(True)
		self.prj_path_name.setText('')
			
	# .....Функция, запускаемая при нажатии кнопки "выбрать существующую"......#
		
	def on_chc_clicked(self):
		global prj_path_cur
		global pickles_dir
		global pd_2

		prj_dir = QFileDialog.getExistingDirectory(self, directory=full_dir + '/system/')
		prj_path_cur, pickles_dir = os.path.split(prj_dir)

		pd_1, pd_2 = pickles_dir.split("_")

		initial_path = prj_dir + '/' + 'initial.pkl'
		
		if os.path.exists(initial_path) == True: 
			self.prj_path_name.setText(prj_dir)
			self.save_button.setEnabled(True)
			self.mesh_name.setText(pd_1)
			if pd_2 == 'blockMesh':
				self.bm.setChecked(True)
				par.on_mesh_type_get(pd_2)
			elif pd_2 == 'snappyHexMesh':
				self.shm.setChecked(True)
				par.on_mesh_type_get(pd_2)
				
			self.prj_frame.setEnabled(True)
			self.prj_path_name.setEnabled(False)
		else:
			if int_lng == 'Russian':
				dialog = QMessageBox(QMessageBox.Critical, "Внимание!", "Это не директория сетки или в ней отсутствуют все необходимые файлы", buttons = QMessageBox.Ok)
			elif int_lng == 'English':
				dialog = QMessageBox(QMessageBox.Critical, "Attention!", "This is not a grid directory, or all necessary files are missing in it", buttons = QMessageBox.Ok)
			result = dialog.exec_()			
		
	# ....................Функция, запускаемая при нажатии кнопки "сохранить"....................#

	def on_save_clicked(self):
		global pckls_path

		msh_lbl_widget = par.tdw_grid.itemAtPosition(0, 2)
		msh_path_lbl_widget = par.tdw_grid.itemAtPosition(0, 3)

		if msh_lbl_widget != None:
			par.tdw_grid.removeWidget(msh_lbl_widget, 0, 2)
		if msh_path_lbl_widget != None:
			par.tdw_grid.removeWidget(msh_path_lbl_widget, 0, 3)
		
		full_dir = par.full_dir
		if self.radio_1.isChecked():
			
			f = open(full_dir+'/MESH_BASH', 'w')
			if self.fmtf_radio.isChecked():
				f.write('#!/bin/sh' + '\n' + '. /opt/openfoam4/etc/bashrc' + '\n' + 'fluentMeshToFoam ' + mesh_dir + '\n' + 'exit')
				f.close()

			elif self.f3Dmtf_radio.isChecked():
				f.write('#!/bin/sh' + '\n' + '. /opt/openfoam4/etc/bashrc' + '\n' + 'fluent3DMeshToFoam ' + mesh_dir + '\n' + 'exit')
				f.close()
                
			self.t1.start()

			shutil.copytree("./matches/0", full_dir + "/0")

			par.msh_visual.setEnabled(True)
		
		elif self.radio_2.isChecked():
			global mesh_name_txt
		
			easy_lbl = QLabel()
			par.cdw.setTitleBarWidget(easy_lbl)
			par.cdw.setWidget(easy_lbl)

			mesh_name_txt = self.mesh_name.text()
			msh_lbl = QLabel()
			if int_lng == 'Russian':
				msh_lbl.setText('Путь до расчетной сетки:')
			elif int_lng == 'English':
				msh_lbl.setText('Path to mesh file:')

			if self.bm.isChecked() == True:
				pd_2 = 'blockMesh'
			elif self.shm.isChecked() == True:
				pd_2 = 'snappyHexMesh'
				
			msh_lbl.setStyleSheet("border-style: none;" "font-size: 10pt;")
			msh_path_lbl = QLineEdit()
			msh_path_lbl.setStyleSheet("background-color: white;" "font-size: 10pt;" "color: green;")
			msh_path_lbl.setFixedSize(500, 25)
			msh_path_lbl.setText(par.full_dir + '/system/' + mesh_name_txt + "_" + pd_2)
			msh_path_lbl.setEnabled(False)

			par.tdw_grid.addWidget(msh_lbl, 0, 2, alignment=QtCore.Qt.AlignCenter)
			par.tdw_grid.addWidget(msh_path_lbl, 0, 3, alignment=QtCore.Qt.AlignCenter)

			self.clear_label = QLabel()
			if self.nf_radio.isChecked() == True:
				if self.mesh_name.text() == '':
					if int_lng == 'Russian':
						dialog = QMessageBox(QMessageBox.Critical, "Внимание!", "Укажите название сетки", buttons = QMessageBox.Ok)
					elif int_lng == 'English':
						dialog = QMessageBox(QMessageBox.Critical, "Attention!", "Specify name mesh", buttons = QMessageBox.Ok)
					result = dialog.exec_()
				else:
					
					if self.bm.isChecked() == True:
						par.addDockWidget(QtCore.Qt.BottomDockWidgetArea, par.serv_mes)
						pckls_path = full_dir + '/system/'
						pd_2_cur = 'blockMesh'
						bmd_form = bmd_window_class(self, par, pckls_path, mesh_name_txt, pd_2_cur)
						par.ffw.setWidget(bmd_form)
						self.close()

						par.cdw.setWidget(self.clear_label)
						par.cdw.setTitleBarWidget(self.clear_label)

						par.setCentralWidget(par.ffw)

						ffw_label = QLabel()
						par.ffw.setTitleBarWidget(par.ffw_frame)
						par.ffw_label.setText(
							"Форма подготовки расчетной сетки: " + "<font color='peru'>" + 'blockMesh' + "</font>")
						par.ffw_label.setStyleSheet("border-style: none;" "font-size: 9pt;")
						
						dir_system_name = os.path.basename(full_dir + '/system')
						if dir_system_name:
							item_system = QtGui.QStandardItem(dir_system_name)
						
							el_system = 'blockMeshDict'
							child_item_system = QtGui.QStandardItem(el_system)
							child_item_system.setForeground(QtGui.QColor('navy'))
							item_system.setChild(3, 0, child_item_system)

						if os.path.basename(full_dir + '/system/blockMeshDict'):
							dir_0_name = os.path.basename(full_dir + '/0')

							item_0 = QtGui.QStandardItem(dir_0_name)
							files_0 = ['D', 'T']
							j = 0
							index = par.treeview.model.index(2, 0)
							par.treeview.expand(index)
							for el_0 in files_0:
								child_item_0 = QtGui.QStandardItem(el_0)
								child_item_0.setForeground(QtGui.QColor('navy'))
								item_0.setChild(j, 0, child_item_0)
								j = j + 1
							
					elif self.shm.isChecked() == True:
						par.addDockWidget(QtCore.Qt.BottomDockWidgetArea, par.serv_mes)
						pckls_path = full_dir + '/system/'
						pd_2_cur = 'snappyHexMesh'
						shmd_form = shmd_window_class(self, par, pckls_path, mesh_name_txt, pd_2_cur)
						par.ffw.setWidget(shmd_form)
						self.close()

						par.cdw.setWidget(self.clear_label)
						par.cdw.setTitleBarWidget(self.clear_label)

						par.setCentralWidget(par.ffw)

						ffw_label = QLabel()
						par.ffw.setTitleBarWidget(par.ffw_frame)
						par.ffw_label.setText(
							"Форма подготовки расчетной сетки: " + "<font color='peru'>" + 'snappyHexMesh' + "</font>")
						par.ffw_label.setStyleSheet("border-style: none;" "font-size: 9pt;")
						
						dir_system_name = os.path.basename(full_dir + '/system/snappyHexMeshDict')
						if dir_system_name:
							item_system = QtGui.QStandardItem(dir_system_name)
						
							el_system = 'snappyHexMeshDict'
							child_item_system = QtGui.QStandardItem(el_system)
							child_item_system.setForeground(QtGui.QColor('navy'))
							item_system.setChild(3, 0, child_item_system)

						if os.path.basename(full_dir + '/system/snappyHexMeshDict'):
							dir_0_name = os.path.basename(full_dir + '/0')

							item_0 = QtGui.QStandardItem(dir_0_name)
							files_0 = ['D', 'T']
							j = 0
							index = par.treeview.model.index(2, 0)
							par.treeview.expand(index)
							for el_0 in files_0:
								child_item_0 = QtGui.QStandardItem(el_0)
								child_item_0.setForeground(QtGui.QColor('navy'))
								item_0.setChild(j, 0, child_item_0)
								j = j + 1
					
					if os.path.exists(pckls_path + self.mesh_name.text()) == True:
						msh_msg_box = QMessageBox()
						if int_lng == 'Russian':
							msh_msg_box.setText("Расчетная сетка с таким именем существует")
							msh_msg_box.setInformativeText("Заменить существующую сетку?")
						elif int_lng == 'English':
							msh_msg_box.setText("A calculated mesh with this name exists")
							msh_msg_box.setInformativeText("Replace an existing mesh?")

						msh_msg_box.setStandardButtons(QMessageBox.Save | QMessageBox.Discard)
						msh_msg_box.setDefaultButton(QMessageBox.Save)
						ret = msh_msg_box.exec_()
						
						if ret == QMessageBox.Save:
    						# Save was clicked
							shutil.rmtree(pckls_path)
							self.close()
						elif ret == QMessageBox.Discard:
    						# Don't save was clicked
							self.close()
							
			elif self.cf_radio.isChecked() == True:	
				
				if pd_2 == 'blockMesh':

					par.addDockWidget(QtCore.Qt.BottomDockWidgetArea, par.serv_mes)
					pckls_path = full_dir + '/system/'
					pd_2_cur = 'blockMesh'
					bmd_form = bmd_window_class(self, par, pckls_path, mesh_name_txt, pd_2_cur)
					par.ffw.setWidget(bmd_form)
					
					self.close()

					par.cdw.setWidget(self.clear_label)
					par.cdw.setTitleBarWidget(self.clear_label)

					par.setCentralWidget(par.ffw)

					ffw_label = QLabel()
					par.ffw.setTitleBarWidget(par.ffw_frame)
					par.ffw_label.setText(
						"Форма подготовки расчетной сетки: " + "<font color='peru'>" + 'blockMesh' + "</font>")
					par.ffw_label.setStyleSheet("border-style: none;" "font-size: 9pt;")

					dir_system_name = os.path.basename(full_dir + '/system')
					if dir_system_name:
						item_system = QtGui.QStandardItem(dir_system_name)

						el_system = 'blockMeshDict'
						child_item_system = QtGui.QStandardItem(el_system)
						child_item_system.setForeground(QtGui.QColor('navy'))
						item_system.setChild(3, 0, child_item_system)

					if os.path.basename(full_dir + '/system/blockMeshDict'):
						dir_0_name = os.path.basename(full_dir + '/0')

						item_0 = QtGui.QStandardItem(dir_0_name)
						files_0 = ['D', 'T']
						j = 0
						index = par.treeview.model.index(2, 0)
						par.treeview.expand(index)
						for el_0 in files_0:
							child_item_0 = QtGui.QStandardItem(el_0)
							child_item_0.setForeground(QtGui.QColor('navy'))
							item_0.setChild(j, 0, child_item_0)
							j = j + 1
								
					el_system = 'blockMeshDict'
					item_system = par.treeview.model.item(1, 0)
					child_item_system = QtGui.QStandardItem(el_system)
					child_item_system.setForeground(QtGui.QColor('navy'))
					item_system.setChild(3, 0, child_item_system)

				elif pd_2 == 'snappyHexMesh':
					
					par.addDockWidget(QtCore.Qt.BottomDockWidgetArea, par.serv_mes)
					pckls_path = full_dir + '/system/'
					pd_2_cur = 'snappyHexMesh'
					shmd_form = shmd_window_class(self, par, pckls_path, mesh_name_txt, pd_2_cur)
					par.ffw.setWidget(shmd_form)

					if os.path.exists(pckls_path + '/snappyHexMeshDict'):
						outf = open(pckls_path + '/snappyHexMeshDict')
						data = outf.read()
						if int_lng == 'Russian':
							par.outf_lbl.setText("Файл: " + "<font color='peru'>" + 'snappyHexMeshDict' + "</font>") 
						elif int_lng == 'English':
							par.outf_lbl.setText("<font color='peru'>" + 'snappyHexMeshDict' + "</font>" + " file") 
						par.outf_edit.setText(data)
						par.cdw.setWidget(par.outf_scroll)

						par.cdw.setTitleBarWidget(par.cdw_frame)
					else:
						empty_lbl = QLabel()
						par.cdw.setWidget(empty_lbl)
						par.cdw.setTitleBarWidget(empty_lbl)
					
					el_system = 'snappyHexMeshDict'
					item_system = par.treeview.model.item(1, 0)
					child_item_system = QtGui.QStandardItem(el_system)
					child_item_system.setForeground(QtGui.QColor('navy'))
					item_system.setChild(3, 0, child_item_system)
				
				if int_lng == 'Russian':
					msg_lbl = QLabel('<span style="color:blue">' + 'Загружены параметры сетки ' + self.mesh_name.text() + '. Установите ее в качестве текущей, выполнив генерацию сетки' + '</span>')
				elif int_lng == 'English':
					msg_lbl = QLabel('<span style="color:blue">' + 'Loaded parameters of mesh ' + self.mesh_name.text() + '. Set it as current, making mesh generation' + '</span>')
					
				par.listWidget.clear()
				par.item = QListWidgetItem()
				par.listWidget.addItem(par.item)
				par.listWidget.setItemWidget(par.item, msg_lbl)
				
				self.close()

				par.msh_run.setEnabled(True)
				par.msh_visual.setEnabled(True)
				par.str_an_run.setEnabled(True)
				par.str_an_vis_run.setEnabled(True)
				par.on_prj_path_get(prj_path_cur, mesh_name_txt)
	
	def int_lng_path_return(self):
		return(int_lng)

# .....................Функция, запускаемая при нажатии кнопки "отмена"......................#
        
	def on_cancel_clicked(self):
		self.close()
		
		
		
		
		