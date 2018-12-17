# -*- coding: utf-8 -*-
# -----------------------------Импорт модулей-----------------------------------

from PyQt5 import QtSql
import os
import os.path
import shutil

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout, QTableWidget, QComboBox, \
    QSpinBox, QPushButton, QListWidgetItem

# -----------------------------------Форма--------------------------------------

class fvSchemes_form_class(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.interface_lng_val = parent.interface_lng_val
        self.con = parent.con
        self.full_dir = parent.full_dir
        self.par = parent

        if self.con.open():

            table = QTableWidget(12, 2)
            table.setColumnWidth(0, 250)
            table.setColumnWidth(1, 230)
            table.setFixedSize(674, 480)
            table.setHorizontalHeaderLabels(["Параметр", "Значение"])

            # d2dt2Schemes.default
            d2dt2Schemes_default_lbl = QLabel('d2dt2Schemes.default')
            self.d2dt2Schemes_default = QComboBox()
            d2dt2Schemes_default_list = ["steadyState", "demo"]
            self.d2dt2Schemes_default.addItems(d2dt2Schemes_default_list)
            table.setCellWidget(0, 1, self.d2dt2Schemes_default)
            table.setCellWidget(0, 0, d2dt2Schemes_default_lbl)

            # ddtSchemes.default
            ddtSchemes_default_lbl = QLabel('ddtSchemes.default')
            self.ddtSchemes_default = QComboBox()
            ddtSchemes_default_list = ["Euler", "demo"]
            self.ddtSchemes_default.addItems(ddtSchemes_default_list)
            table.setCellWidget(1, 1, self.ddtSchemes_default)
            table.setCellWidget(1, 0, ddtSchemes_default_lbl)

            # gradSchemes.default
            gradSchemes_default_lbl = QLabel('gradSchemes.default')
            self.gradSchemes_default = QComboBox()
            gradSchemes_default_list = ["leastSquares", "demo"]
            self.gradSchemes_default.addItems(gradSchemes_default_list)
            table.setCellWidget(2, 1, self.gradSchemes_default)
            table.setCellWidget(2, 0, gradSchemes_default_lbl)

            # gradSchemes.grad(D)
            gradSchemes_grad_D_lbl = QLabel('gradSchemes.grad(D)')
            self.gradSchemes_grad_D = QComboBox()
            gradSchemes_grad_D_list = ["leastSquares", "demo"]
            self.gradSchemes_grad_D.addItems(gradSchemes_grad_D_list)
            table.setCellWidget(3, 1, self.gradSchemes_grad_D)
            table.setCellWidget(3, 0, gradSchemes_grad_D_lbl)

            # gradSchemes.grad(T)
            gradSchemes_grad_T_lbl = QLabel('gradSchemes.grad(T)')
            self.gradSchemes_grad_T = QComboBox()
            gradSchemes_grad_T_list = ["leastSquares", "demo"]
            self.gradSchemes_grad_T.addItems(gradSchemes_grad_T_list)
            table.setCellWidget(4, 1, self.gradSchemes_grad_T)
            table.setCellWidget(4, 0, gradSchemes_grad_T_lbl)

            # divSchemes.default
            divSchemes_default_lbl = QLabel('divSchemes.default')
            self.divSchemes_default = QComboBox()
            divSchemes_default_list = ["none", "demo"]
            self.divSchemes_default.addItems(divSchemes_default_list)
            table.setCellWidget(5, 1, self.divSchemes_default)
            table.setCellWidget(5, 0, divSchemes_default_lbl)

            # divSchemes.div(sigmaD)
            divSchemes_div_sigmaD_lbl = QLabel('divSchemes.div(sigmaD)')
            self.divSchemes_div_sigmaD = QComboBox()
            divSchemes_div_sigmaD_list = ["Gauss linear", "demo"]
            self.divSchemes_div_sigmaD.addItems(divSchemes_div_sigmaD_list)
            table.setCellWidget(6, 1, self.divSchemes_div_sigmaD)
            table.setCellWidget(6, 0, divSchemes_div_sigmaD_lbl)

            # laplacianSchemes.default
            laplacianSchemes_default_lbl = QLabel('laplacianSchemes.default')
            self.laplacianSchemes_default = QComboBox()
            laplacianSchemes_default_list = ["none", "demo"]
            self.laplacianSchemes_default.addItems(laplacianSchemes_default_list)
            table.setCellWidget(7, 1, self.laplacianSchemes_default)
            table.setCellWidget(7, 0, laplacianSchemes_default_lbl)

            # laplacianSchemes.laplacian(DD,D)
            laplacianSchemes_laplacian_DD_D_lbl = QLabel('laplacianSchemes.laplacian(DD,D)')
            self.laplacianSchemes_laplacian_DD_D = QComboBox()
            laplacianSchemes_laplacian_DD_D_list = ["Gauss linear corrected", "demo"]
            self.laplacianSchemes_laplacian_DD_D.addItems(laplacianSchemes_laplacian_DD_D_list)
            table.setCellWidget(8, 1, self.laplacianSchemes_laplacian_DD_D)
            table.setCellWidget(8, 0, laplacianSchemes_laplacian_DD_D_lbl)

            # laplacianSchemes.laplacian(DT,T)
            laplacianSchemes_laplacian_DT_T_lbl = QLabel('laplacianSchemes.laplacian(DT,T)')
            self.laplacianSchemes_laplacian_DT_T = QComboBox()
            laplacianSchemes_laplacian_DT_T_list = ["Gauss linear corrected", "demo"]
            self.laplacianSchemes_laplacian_DT_T.addItems(laplacianSchemes_laplacian_DT_T_list)
            table.setCellWidget(9, 1, self.laplacianSchemes_laplacian_DT_T)
            table.setCellWidget(9, 0, laplacianSchemes_laplacian_DT_T_lbl)

            # interpolationSchemes.default
            interpolationSchemes_default_lbl = QLabel('interpolationSchemes.default')
            self.interpolationSchemes_default = QComboBox()
            interpolationSchemes_default_list = ["linear", "demo"]
            self.interpolationSchemes_default.addItems(interpolationSchemes_default_list)
            table.setCellWidget(10, 1, self.interpolationSchemes_default)
            table.setCellWidget(10, 0, interpolationSchemes_default_lbl)

            # snGradSchemes.default
            snGradSchemes_default_lbl = QLabel('snGradSchemes.default')
            self.snGradSchemes_default = QComboBox()
            snGradSchemes_default_list = ["demo", "none"]
            self.snGradSchemes_default.addItems(snGradSchemes_default_list)
            table.setCellWidget(11, 1, self.snGradSchemes_default)
            table.setCellWidget(11, 0, snGradSchemes_default_lbl)

            # вывод значений параметров
            if 'fvSchemes' in self.con.tables():
						
                query = QtSql.QSqlQuery()
                query.exec("SELECT * FROM fvSchemes")
                if query.isActive():
                    query.first()
                    value_list = []
                    while query.isValid():
                        value_res = query.value('value')
                        value_list.append(value_res)
                        query.next()
					
                    # d2dt2Schemes_default
                    d2dt2Schemes_default_mas = self.d2dt2Schemes_default.count()   
                    for i in range(d2dt2Schemes_default_mas):
                        if self.d2dt2Schemes_default.itemText(i) == value_list[0]:
                            self.d2dt2Schemes_default.setCurrentIndex(i)
							
                    # ddtSchemes_default
                    ddtSchemes_default_mas = self.ddtSchemes_default.count()   
                    for i in range(ddtSchemes_default_mas):
                        if self.ddtSchemes_default.itemText(i) == value_list[1]:
                            self.ddtSchemes_default.setCurrentIndex(i)
							
                    # gradSchemes_default
                    gradSchemes_default_mas = self.gradSchemes_default.count()   
                    for i in range(gradSchemes_default_mas):
                        if self.gradSchemes_default.itemText(i) == value_list[2]:
                            self.gradSchemes_default.setCurrentIndex(i)
							
                    # gradSchemes_grad_D
                    gradSchemes_grad_D_mas = self.gradSchemes_grad_D.count()   
                    for i in range(gradSchemes_grad_D_mas):
                        if self.gradSchemes_grad_D.itemText(i) == value_list[3]:
                            self.gradSchemes_grad_D.setCurrentIndex(i)
							
                    # gradSchemes_grad_T
                    gradSchemes_grad_T_mas = self.gradSchemes_grad_T.count()   
                    for i in range(gradSchemes_grad_T_mas):
                        if self.gradSchemes_grad_T.itemText(i) == value_list[4]:
                            self.gradSchemes_grad_T.setCurrentIndex(i)
							
                    # divSchemes_default
                    divSchemes_default_mas = self.divSchemes_default.count()   
                    for i in range(divSchemes_default_mas):
                        if self.divSchemes_default.itemText(i) == value_list[5]:
                            self.divSchemes_default.setCurrentIndex(i)
							
                    # divSchemes_div_sigmaD
                    divSchemes_div_sigmaD_mas = self.divSchemes_div_sigmaD.count()   
                    for i in range(divSchemes_div_sigmaD_mas):
                        if self.divSchemes_div_sigmaD.itemText(i) == value_list[6]:
                            self.divSchemes_div_sigmaD.setCurrentIndex(i)
							
                    # laplacianSchemes_default
                    laplacianSchemes_default_mas = self.laplacianSchemes_default.count()   
                    for i in range(laplacianSchemes_default_mas):
                        if self.laplacianSchemes_default.itemText(i) == value_list[7]:
                            self.laplacianSchemes_default.setCurrentIndex(i)
							
                    # laplacianSchemes_laplacian_DD_D
                    laplacianSchemes_laplacian_DD_D_mas = self.laplacianSchemes_laplacian_DD_D.count()   
                    for i in range(laplacianSchemes_laplacian_DD_D_mas):
                        if self.laplacianSchemes_laplacian_DD_D.itemText(i) == value_list[8]:
                            self.laplacianSchemes_laplacian_DD_D.setCurrentIndex(i)
							
                    # laplacianSchemes_laplacian_DT_T
                    laplacianSchemes_laplacian_DT_T_mas = self.laplacianSchemes_laplacian_DT_T.count()   
                    for i in range(laplacianSchemes_laplacian_DT_T_mas):
                        if self.laplacianSchemes_laplacian_DT_T.itemText(i) == value_list[9]:
                            self.laplacianSchemes_laplacian_DT_T.setCurrentIndex(i)
							
												
                    # interpolationSchemes_default
                    interpolationSchemes_default_mas = self.interpolationSchemes_default.count()   
                    for i in range(interpolationSchemes_default_mas):
                        if self.interpolationSchemes_default.itemText(i) == value_list[10]:
                            self.interpolationSchemes_default.setCurrentIndex(i)
							
                    # snGradSchemes_default
                    snGradSchemes_default_mas = self.snGradSchemes_default.count()   
                    for i in range(snGradSchemes_default_mas):
                        if self.snGradSchemes_default.itemText(i) == value_list[11]:
                            self.snGradSchemes_default.setCurrentIndex(i)


            btnSave = QPushButton()
            btnSave.setFixedSize(80, 25)
            btnSave.clicked.connect(self.on_btnSave_clicked)

            if self.interface_lng_val == 'Russian':
                btnSave.setText("Сохранить")
            elif self.interface_lng_val == 'English':
                btnSave.setText("Save")

            vbox = QVBoxLayout()
            vbox.addWidget(table)
            vbox.addWidget(btnSave)

# ---------------------Размещение на форме всех компонентов-------------------------

            form = QFormLayout()
            form.addRow(vbox)
            self.setLayout(form)

    def on_btnSave_clicked(self):
        d2dt2Schemes_default_txt = self.d2dt2Schemes_default.currentText()
        ddtSchemes_default_txt = self.ddtSchemes_default.currentText()
        gradSchemes_default_txt = self.gradSchemes_default.currentText()
        gradSchemes_grad_D_txt = self.gradSchemes_grad_D.currentText()
        gradSchemes_grad_T_txt = self.gradSchemes_grad_T.currentText()
        divSchemes_default_txt = self.divSchemes_default.currentText()
        divSchemes_div_sigmaD_txt = self.divSchemes_div_sigmaD.currentText()
        laplacianSchemes_default_txt = self.laplacianSchemes_default.currentText()
        laplacianSchemes_laplacian_DD_D_txt = self.laplacianSchemes_laplacian_DD_D.currentText()
        laplacianSchemes_laplacian_DT_T_txt = self.laplacianSchemes_laplacian_DT_T.currentText()
        interpolationSchemes_default_txt = self.interpolationSchemes_default.currentText()
        snGradSchemes_default_txt = self.snGradSchemes_default.currentText()
		
        if 'fvSchemes' not in self.con.tables():
            query = QtSql.QSqlQuery()
            query.exec("CREATE TABLE fvSchemes(param, value)")

            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('d2dt2Schemes.default', ''))
            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('ddtSchemes.default', ''))
            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('gradSchemes.default', ''))
            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('gradSchemes.grad(D)', ''))
            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('gradSchemes.grad(T)', ''))
            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('divSchemes.default', ''))
            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('divSchemes.div(sigmaD)', ''))
            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('laplacianSchemes.default', ''))
            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('laplacianSchemes.laplacian(DD,D)', ''))
            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('laplacianSchemes.laplacian(DT,T)', ''))
            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('interpolationSchemes.default', ''))
            query.exec("INSERT INTO fvSchemes(param, value) VALUES ('%s','%s')" % ('snGradSchemes.default', ''))


        if 'fvSchemes' in self.con.tables():
            query = QtSql.QSqlQuery()

            query.prepare("UPDATE fvSchemes SET value=? WHERE param='d2dt2Schemes.default'")
            query.bindValue(0, d2dt2Schemes_default_txt)
            query.exec_()

            query.prepare("UPDATE fvSchemes SET value=? WHERE param='ddtSchemes.default'")
            query.bindValue(0, ddtSchemes_default_txt)
            query.exec_()

            query.prepare("UPDATE fvSchemes SET value=? WHERE param='gradSchemes.default'")
            query.bindValue(0, gradSchemes_default_txt)
            query.exec_()

            query.prepare("UPDATE fvSchemes SET value=? WHERE param='gradSchemes.grad(D)'")
            query.bindValue(0, gradSchemes_grad_D_txt)
            query.exec_()

            query.prepare("UPDATE fvSchemes SET value=? WHERE param='gradSchemes.grad(T)'")
            query.bindValue(0, gradSchemes_grad_T_txt)
            query.exec_()

            query.prepare("UPDATE fvSchemes SET value=? WHERE param='divSchemes.default'")
            query.bindValue(0, divSchemes_default_txt)
            query.exec_()

            query.prepare("UPDATE fvSchemes SET value=? WHERE param='divSchemes.div(sigmaD)'")
            query.bindValue(0, divSchemes_div_sigmaD_txt)
            query.exec_()

            query.prepare("UPDATE fvSchemes SET value=? WHERE param='laplacianSchemes.default'")
            query.bindValue(0, laplacianSchemes_default_txt)
            query.exec_()

            query.prepare("UPDATE fvSchemes SET value=? WHERE param='laplacianSchemes.laplacian(DD,D)'")
            query.bindValue(0, laplacianSchemes_laplacian_DD_D_txt)
            query.exec_()

            query.prepare("UPDATE fvSchemes SET value=? WHERE param='laplacianSchemes.laplacian(DT,T)'")
            query.bindValue(0, laplacianSchemes_laplacian_DT_T_txt)
            query.exec_()

            query.prepare("UPDATE fvSchemes SET value=? WHERE param='interpolationSchemes.default'")
            query.bindValue(0, interpolationSchemes_default_txt)
            query.exec_()

            query.prepare("UPDATE fvSchemes SET value=? WHERE param='snGradSchemes.default'")
            query.bindValue(0, snGradSchemes_default_txt)
            query.exec_()

        # записываем файл fvSchemes
        if os.path.exists(self.full_dir + '/system/fvSchemes'):
            os.remove(self.full_dir + '/system/fvSchemes')
		
        shutil.copyfile("./matches/Shablon/system/fvSchemes", self.full_dir + '/system/fvSchemes')

        fvS = open(self.full_dir + '/system/fvSchemes', 'a')
        ###d2dt2Schemes###
        d2dt2Schemes_bl = '\n' + 'd2dt2Schemes' + '\n' + '{' + '\n' + '     ' + 'default'  + '          ' + d2dt2Schemes_default_txt + ';' + '\n' + '}' + '\n\n'

        ###ddtSchemes###
        ddtSchemes_bl = 'ddtSchemes' + '\n' + '{' + '\n' + '     ' + 'default'  + '          ' + ddtSchemes_default_txt + ';' + '\n' + '}' + '\n\n'

        ###gradSchemes###
        gradSchemes_bl = 'gradSchemes' + '\n' + '{' + '\n' + '     ' + 'default'  + '          ' + gradSchemes_default_txt + ';' + '\n' \
        + '     ' + 'grad(D)' + '          ' + gradSchemes_grad_D_txt + ';' + '\n' \
        + '     ' + 'grad(T)' + '          ' + gradSchemes_grad_T_txt + ';' + '\n' + '}' + '\n\n'

        ###divSchemes###
        divSchemes_bl = 'divSchemes' + '\n' + '{' + '\n' + '     ' + 'default' + '          ' + divSchemes_default_txt + ';' + '\n' \
        + '     ' + 'div(sigmaD)' + '          ' +  divSchemes_div_sigmaD_txt + ';' + '\n' + '}' + '\n\n'

        ###laplacianSchemes###
        laplacianSchemes_bl = 'laplacianSchemes' + '\n' + '{' + '\n' + '     ' + 'default'  + '          ' + laplacianSchemes_default_txt + ';' + '\n' \
        + '     ' + 'laplacian(DD,D)' + '          ' + laplacianSchemes_laplacian_DD_D_txt + ';' + '\n' \
        + '     ' + 'laplacian(DT,T)' + '          ' + laplacianSchemes_laplacian_DT_T_txt + ';' + '\n' + '}' + '\n\n'

        ###interpolationSchemes###
        interpolationSchemes_bl = 'interpolationSchemes' + '\n' + '{' + '\n' + '     ' + 'default' + '          ' + interpolationSchemes_default_txt + ';' + '\n' + '}' + '\n\n'

        ###snGradSchemes###
        snGradSchemes_bl = 'snGradSchemes' + '\n' + '{' + '\n' + '     ' + 'default' + '          ' + snGradSchemes_default_txt + ';' + '\n' + '}' + '\n\n'

        fvS.write(d2dt2Schemes_bl + ddtSchemes_bl + gradSchemes_bl + divSchemes_bl + laplacianSchemes_bl + interpolationSchemes_bl + snGradSchemes_bl)
        close_str = '// ************************************************************************* //'
        fvS.write(close_str)

        fvS.close()

        self.par.cdw.setWidget(self.par.outf_scroll)
        outf = open(self.full_dir + '/system/fvSchemes')

        if self.interface_lng_val == 'Russian':
            msg_lbl = QLabel(
                '<span style="color:green">Файл fvSchemes сохранен</span>')
        elif self.interface_lng_val == 'English':
            msg_lbl = QLabel(
                '<span style="color:green">The fvSchemes file was saved</span>')

        self.par.listWidget.clear()
        self.par.item = QListWidgetItem()
        self.par.listWidget.addItem(self.par.item)
        self.par.listWidget.setItemWidget(self.par.item, msg_lbl)

        data = outf.read()

        if self.interface_lng_val == 'Russian':
            self.par.outf_lbl.setText("Файл " + "<font color='peru'>" + 'fvSchemes' + "</font>")
        elif self.interface_lng_val == 'English':
            self.par.outf_lbl.setText("<font color='peru'>" + 'fvSchemes' + "</font>" + " file")
        self.par.outf_edit.setText(data)

        self.par.cdw.setTitleBarWidget(self.par.cdw_frame)
        outf.close()

