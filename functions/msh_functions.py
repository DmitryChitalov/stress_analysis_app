# -*- coding: utf-8 -*-
#---------------------------Импорт модулей и внешних форм-------------------------#

from PyQt5 import QtCore
from PyQt5 import QtSql
from PyQt5 import QtGui

from PyQt5.QtWidgets import QWidget, QFileDialog, QLineEdit, QLabel, \
    QHBoxLayout, QLineEdit, QPushButton, QGridLayout, \
    QFrame, QVBoxLayout, QFormLayout, QRadioButton, QDoubleSpinBox, \
	QSpinBox, QCheckBox, QGroupBox, QComboBox, QListWidgetItem

import pickle
import os
import shutil
import re

class msh_functions_class():		
	
	###..............................Функция вывода результатов потока t1..........................### 
	
	def on_msh_finished(return_code, prj_path_val_th, mesh_name_txt_val_th, par, int_lng, msh_t):

		msh_read_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th + "/mesh_out.log")
		data = msh_read_file.read()

		if int_lng == 'Russian':
			par.outf_lbl.setText('Результаты генерации сетки типа ' + msh_t) 
		elif int_lng == 'English':
			par.outf_lbl.setText('Generation results of mesh of type ' + msh_t) 
		par.cdw.setWidget(par.outf_scroll)
		par.cdw.setTitleBarWidget(par.cdw_frame)
		par.outf_edit.setText(data)

		if return_code == 0:
			if int_lng == 'Russian':
				msg_lbl = QLabel('<span style="color:green">' + "Расчетная сетка типа " + msh_t + " успешно сгенерирована" + '</span>')
			elif int_lng == 'English':
				msg_lbl = QLabel('<span style="color:green">' + "Mesh of type " + msh_t + " was successfully generated" + '</span>')
			color = QtGui.QColor("green")
			
			par.msh_visual.setEnabled(True)

		else:
			if int_lng == 'Russian':
				msg_lbl = QLabel('<span style="color:red">' + "Расчетная сетка типа " + msh_t + " сгенерирована c ошибками" + '</span>')
			elif int_lng == 'English':
				msg_lbl = QLabel('<span style="color:red">' + "Mesh of type " + msh_t + " was generated with errors" + '</span>')
			color = QtGui.QColor("red")
					
		par.listWidget.clear()
		par.item = QListWidgetItem()
		par.listWidget.addItem(par.item)
		par.listWidget.setItemWidget(par.item, msg_lbl)
		
		if os.path.exists(par.full_dir + '/mesh_script'):
			os.remove(par.full_dir + '/mesh_script')
		if os.path.exists(par.full_dir + '/mesh_out.log'):
			os.remove(par.full_dir + '/mesh_out.log')
		
	def on_msh_visual_run(par, int_lng, msh_t):
		
		if int_lng == 'Russian':
			msg_lbl = QLabel('<span style="color:blue">' + "Визуализация сетки типа " + msh_t + " запущена" + '</span>')
		elif int_lng == 'English':
			msg_lbl = QLabel('<span style="color:blue">' + "Visualisation of the mesh of type " + msh_t + " is started" + '</span>')
					
		par.listWidget.clear()
		par.item = QListWidgetItem()
		par.listWidget.addItem(par.item)
		par.listWidget.setItemWidget(par.item, msg_lbl)
		
	def on_msh_visual_finished(return_code, prj_path_val_th, mesh_name_txt_val_th, par, int_lng, msh_t):

		msh_read_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th + "/mesh_visual_out.log")
		data = msh_read_file.read()

		if int_lng == 'Russian':
			par.outf_lbl.setText('Результаты визуализации сетки типа ' + msh_t) 
		elif int_lng == 'English':
			par.outf_lbl.setText('Vizualization results of mesh of type ' + msh_t) 
		par.cdw.setWidget(par.outf_scroll)
		par.cdw.setTitleBarWidget(par.cdw_frame)
		par.outf_edit.setText(data)

		if return_code == 0:
			if int_lng == 'Russian':
				msg_lbl = QLabel('<span style="color:green">' + "Визуализация сетки " + msh_t + " завершена" + '</span>')
			elif int_lng == 'English':
				msg_lbl = QLabel('<span style="color:green">' + "Mesh visualisation of type " + msh_t + " complete" + '</span>')
			color = QtGui.QColor("green")

		else:
			if int_lng == 'Russian':
				msg_lbl = QLabel('<span style="color:red">' + "При отображении расчетной сетки " + msh_t + " возникли проблемы" + '</span>')
			elif int_lng == 'English':
				msg_lbl = QLabel('<span style="color:red">' + "Mesh visualisation of type " + msh_t + " complete with errors" + '</span>')
			color = QtGui.QColor("red")

		par.listWidget.clear()
		par.item = QListWidgetItem()
		par.listWidget.addItem(par.item)
		par.listWidget.setItemWidget(par.item, msg_lbl)	
		
		if os.path.exists(par.full_dir + '/mesh_visual_script'):
			os.remove(par.full_dir + '/mesh_visual_script')
		if os.path.exists(par.full_dir + '/mesh_visual_out.log'):
			os.remove(par.full_dir + '/mesh_visual_out.log')