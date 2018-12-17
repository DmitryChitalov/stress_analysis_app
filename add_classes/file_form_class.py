# -*- coding: utf-8 -*-
from PyQt5 import QtSql
from PyQt5 import QtCore

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout, QTableWidget, QComboBox, \
    QSpinBox, QPushButton, QListWidgetItem, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout

#---------------------------Импорт модулей и внешних форм-------------------------

from forms.D_form import D_form_class
from forms.T_form import T_form_class
from forms.mechanicalProperties_form import mechanicalProperties_form_class
from forms.thermalProperties_form import thermalProperties_form_class
from forms.controlDict_form import controlDict_form_class
from forms.fvSchemes_form import fvSchemes_form_class
from forms.fvSolution_form import fvSolution_form_class
    
#-------------------------Возврат ссылок на формы параметров----------------------
    
class file_form_class:
    def inp_file_form_func(self, file_name, con):
        global file_form
        global file_name_gl
        
        file_name_gl = file_name
        connection = con
        par = self

        if file_name_gl == "D":
            if 'patches' in connection.tables(): 
                file_form = D_form_class(self)
            else:
                if par.interface_lng_val == 'Russian':
                    msg_lbl = QLabel(
                    '<span style="color:red">Сначала создайте расчетную сетку</span>')
                elif par.interface_lng_val == 'English':
                    msg_lbl = QLabel(
                    '<span style="color:red">Make the computational mesh</span>')

                par.listWidget.clear()
                par.item = QListWidgetItem()
                par.listWidget.addItem(par.item)
                par.listWidget.setItemWidget(par.item, msg_lbl)
				
                file_name_gl = None
                file_form = None
				
        elif  file_name_gl == "T":
            if 'patches' in connection.tables(): 
                file_form = T_form_class(self)
            else:
                if par.interface_lng_val == 'Russian':
                    msg_lbl = QLabel(
                    '<span style="color:red">Сначала создайте расчетную сетку</span>')
                elif par.interface_lng_val == 'English':
                    msg_lbl = QLabel(
                    '<span style="color:red">Make the computational mesh</span>')

                par.listWidget.clear()
                par.item = QListWidgetItem()
                par.listWidget.addItem(par.item)
                par.listWidget.setItemWidget(par.item, msg_lbl)
				
                file_name_gl = None
                file_form = None
			
        elif  file_name_gl == "mechanicalProperties":
            file_form = mechanicalProperties_form_class(self)

        elif  file_name_gl == "thermalProperties":
            file_form = thermalProperties_form_class(self)

        elif  file_name_gl == "controlDict":
            file_form = controlDict_form_class(self)

        elif  file_name_gl == "fvSchemes":
            file_form = fvSchemes_form_class(self)

        elif  file_name_gl == "fvSolution":
            file_form = fvSolution_form_class(self)

        else:
            file_name_gl = None
            file_form = None
          
    def out_file_name_func(): return file_name_gl
    def out_file_form_func(): return file_form


