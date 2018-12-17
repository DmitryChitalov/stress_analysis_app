# -*- coding: utf-8 -*-
#---------------------------Импорт модулей и внешних форм-------------------------#

from PyQt5 import QtCore
from PyQt5 import QtSql
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal

from PyQt5.QtWidgets import QWidget, QFileDialog, QLineEdit, QLabel, \
    QHBoxLayout, QLineEdit, QPushButton, QGridLayout, \
    QFrame, QVBoxLayout, QFormLayout, QRadioButton, QDoubleSpinBox, \
	QSpinBox, QCheckBox, QGroupBox, QComboBox, QListWidgetItem

import os
import subprocess
import time

class msh_generation_thread(QtCore.QThread):
	msh_run_sig = pyqtSignal(int, 'QString', 'QString', 'PyQt_PyObject', 'QString', 'QString')
	
	def __init__(self, prj_path_val, mesh_name_txt_val, pp_dir, parent, interface_lng_val, msh_type):
		QtCore.QThread.__init__(self, parent)
		
		global prj_path_val_th
		global mesh_name_txt_val_th_a
		global mesh_name_txt_val_th_new
		global pp_dir_th
		global par
		global int_lng
		global msh_t

		prj_path_val_th = prj_path_val
		mesh_name_txt_val_th_new = mesh_name_txt_val
		pp_dir_th = pp_dir
		par = parent
		int_lng = interface_lng_val
		msh_t = msh_type
		
	def run(self):
		MeshDict_file = prj_path_val_th + '/' + msh_t + "Dict"
		if os.path.exists(MeshDict_file) == True:
			if msh_t == 'blockMesh':
				mesh_name_txt_val_th_a = mesh_name_txt_val_th_new + '_blockMesh'
				msh_bash_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th_a + '/' + 'mesh_script', 'w')
				msh_bash_file.write('#!/bin/sh' + '\n' + '. /opt/openfoam6/etc/bashrc' + '\n' + msh_t + '\n' + 'exit')
				msh_bash_file.close()
			elif msh_t == 'snappyHexMesh':
				mesh_name_txt_val_th_a = mesh_name_txt_val_th_new + '_snappyHexMesh'
				msh_bash_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th_a + '/' + 'mesh_script', 'w')
				msh_bash_file.write('#!/bin/sh' + '\n' + '. /opt/openfoam6/etc/bashrc' + '\n' + 'blockMesh' + '\n' + 'surfaceFeatureExtract' + '\n' + msh_t + '\n' + 'exit')
				msh_bash_file.close()
				
			msh_out_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th_a + '/' + 'mesh_out.log', "w")
			msh_run_subprocess = subprocess.Popen(["bash " + prj_path_val_th + '/' + mesh_name_txt_val_th_a + "/" + "mesh_script"], cwd = pp_dir_th, shell=True, stdout=msh_out_file, stderr=msh_out_file)
			msh_out_file.close()
			
			if int_lng == 'Russian':
				msg_lbl = QLabel('<span style="color:blue">' + "Выполняется генерация расчетной сетки типа " + msh_t + '</span>')
			elif int_lng == 'English':
				msg_lbl = QLabel('<span style="color:blue">' + "Making the generation of mesh of type " + msh_t + '</span>')
					
			par.listWidget.clear()
			par.item = QListWidgetItem()
			par.listWidget.addItem(par.item)
			par.listWidget.setItemWidget(par.item, msg_lbl)
			
			while msh_run_subprocess.poll() is None:
				self.sleep(0.5)
				
			return_code = msh_run_subprocess.returncode

			self.msh_run_sig.emit(return_code, prj_path_val_th, mesh_name_txt_val_th_a, par, int_lng, msh_t)

		else:
			
			if int_lng == 'Russian':
				msg_lbl = QLabel('<span style="color:blue">' + "Выполните сохранение расчетной сетки - файл " + msh_t + '</span>')
			elif int_lng == 'English':
				msg_lbl = QLabel('<span style="color:blue">' + "Save the mesh - " + msh_t + "file"+ '</span>')
					
			par.listWidget.clear()
			par.item = QListWidgetItem()
			par.listWidget.addItem(par.item)
			par.listWidget.setItemWidget(par.item, msg_lbl)
			
			
class msh_visualisation_thread(QtCore.QThread):
	msh_run_vis_start_sig = pyqtSignal('PyQt_PyObject', 'QString', 'QString')
	msh_run_vis_finish_sig = pyqtSignal(int, 'QString', 'QString', 'PyQt_PyObject', 'QString', 'QString')
	def __init__(self, prj_path_val, mesh_name_txt_val, pp_dir, parent, interface_lng_val, msh_type):
		QtCore.QThread.__init__(self, parent)
		
		global prj_path_val_th
		global mesh_name_txt_val_th_a
		global mesh_name_txt_val_th_new
		global pp_dir_th
		global par
		global int_lng
		global msh_t

		prj_path_val_th = prj_path_val
		mesh_name_txt_val_th_new = mesh_name_txt_val
		pp_dir_th = pp_dir
		par = parent
		int_lng = interface_lng_val
		msh_t = msh_type
		
	def run(self):
		self.msh_run_vis_start_sig.emit(par, int_lng, msh_t)
		
		if msh_t == 'blockMesh':
			mesh_name_txt_val_th_a = mesh_name_txt_val_th_new + '_blockMesh'
			MeshDict_file = pp_dir_th + '/' + 'system' + '/' + 'blockMeshDict'
			
		elif msh_t == 'snappyHexMesh':
			mesh_name_txt_val_th_a = mesh_name_txt_val_th_new + '_snappyHexMesh'
			MeshDict_file = pp_dir_th + '/' + 'system' + '/' + 'snappyHexMeshDict'

		if os.path.exists(MeshDict_file) == True:
			msh_viual_bash_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th_a + '/' + 'mesh_visual_script', 'w')
			msh_viual_bash_file.write('#!/bin/sh' + '\n' + '. /opt/openfoam6/etc/bashrc' + '\n' + 'paraFoam' + '\n' + 'exit')
			msh_viual_bash_file.close()

			msh_viual_out_file = open(prj_path_val_th + '/' + mesh_name_txt_val_th_a + '/' + 'mesh_visual_out.log', "w")
			msh_viual_run_subprocess = subprocess.Popen(["bash " + prj_path_val_th + '/' + mesh_name_txt_val_th_a + "/" + "mesh_visual_script"], cwd = pp_dir_th, shell=True, stdout=msh_viual_out_file, stderr=msh_viual_out_file)
			msh_viual_out_file.close()

			while msh_viual_run_subprocess.poll() is None:
				self.sleep(0.5)
			
			return_code = msh_viual_run_subprocess.returncode
			
			self.msh_run_vis_finish_sig.emit(return_code, prj_path_val_th, mesh_name_txt_val_th_a, par, int_lng, msh_t)
				
		else:

			if int_lng == 'Russian':
				msg_lbl = QLabel('<span style="color:red">' + 'Выполните генерацию расчетной сетки' + '</span>')
			elif int_lng == 'English':
				msg_lbl = QLabel('<span style="color:red">' + 'Run mesh generation' + '</span>')
					
			par.listWidget.clear()
			par.item = QListWidgetItem()
			par.listWidget.addItem(par.item)
			par.listWidget.setItemWidget(par.item, msg_lbl)