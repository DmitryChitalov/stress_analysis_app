# -*- coding: utf-8 -*-
#---------------------------Импорт модулей и внешних форм-------------------------#

from PyQt5 import QtCore
from PyQt5 import QtSql
from PyQt5 import QtGui
import pickle
import os
import shutil
import re
import signal

from windows.prj_window import prj_window_class
from windows.lng_window import lng_form_class

class first_toolbar_functions_class():
	
	#.......................Функция открытия окна выбора директории проекта...................
	
    def on_proj_open(par):
        proj_win = prj_window_class(par)
        if par.interface_lng_val == 'Russian':
            proj_win.setWindowTitle('Окно выбора директории проекта')
        elif par.interface_lng_val == 'English':
            proj_win.setWindowTitle('Window for selecting project directory')
        proj_win.show()
		
    #........................Функция открытия окна выбора интерфейса программы...................
        
    def on_lng_chs(par):
        lng_win = lng_form_class(par)
        if par.interface_lng_val == 'Russian':
            lng_win.setWindowTitle('Окно выбора языка интерфейса')
        elif par.interface_lng_val == 'English':
            lng_win.setWindowTitle('Interface language selection window')
        lng_win.show()