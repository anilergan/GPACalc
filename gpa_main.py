
from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QMessageBox, QSpinBox, QLineEdit, QComboBox
from gpa_qt import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets, QtGui
import csv
import pandas as pd


class AppWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        # signal-slot
        self.ui.button_ders_ekle.clicked.connect(self.func_ders_ekle)
        self.ui.button_hesapla.clicked.connect(self.func_hesapla)
        self.ui.button_tumunu_sil.clicked.connect(self.func_tumunu_sil)
        self.ui.button_kaydet.clicked.connect(self.func_kaydet)

        #read database
        self.read_database()


    

    def func_kaydet(self):
        self.dic1 = {'complated_credit': None, 'current_agno': None}
        
        self.tamam_kredi = self.ui.spinbox_input_kredi.value()
        self.guncel_agno = self.ui.spinbox_input_agno.value()

        self.dic1.update({'complated_credit': self.tamam_kredi, 
                             'current_agno': self.guncel_agno})


        with open('db1.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(self.dic1.keys())
            writer.writerow(str(value) for value in self.dic1.values())

        # hiç ders eklenmiş mi kontrol edelim, ekliyse kaç tane ekli?
        self.index = -1
        for child in self.ui.frame_scrollArea_content.children():
            if isinstance(child, QFrame):
                self.index += 1
        
        # eğer ders eklenmişse veri tabanına (db2.csv) kaydedelim
        if self.index > 0:
            self.df = pd.DataFrame(columns=['lesson', 'score', 'credit'])
            for index in range(0,self.index):
                self.lesson_object_name = f"lesson_name_{index}"
                self.lesson = self.findChild(QLineEdit, self.lesson_object_name).text()
                if self.lesson.strip() == '':
                    QMessageBox.critical(self, 'Kayıt Gerçekleşemedi!', 'Ders adi boş bırakılamaz!')
                    return None
                    
                self.score_object_name = f"lesson_score_{index}"
                self.score = self.findChild(QComboBox, self.score_object_name).currentText()

                self.credit_object_name = f"lesson_credit_{index}"
                self.credit = self.findChild(QSpinBox, self.credit_object_name).value()

                self.dic = {
                    'lesson': [self.lesson],
                    'score': [self.score],
                    'credit': [self.credit]
                }

                self.new_data = pd.DataFrame(self.dic)
                self.df = pd.concat([self.df, self.new_data], ignore_index=True)

                self.df.to_csv('db2.csv', index=False, header=True)
            QMessageBox.information(self,'Kayıt Başarılı!', 'Kayıt işlemi başarılı')

        else: 
            self.empty_df = pd.DataFrame(columns=['lesson' ,'score' ,'credit'])
            self.empty_df.to_csv('db2.csv', index=False, header=True)
            QMessageBox.information(self,'Kayıt Başarılı!', 'Kayıt işlemi başarılı')




            

                



    

    def func_ders_ekle(self):
        self.index = -1
        for child in self.ui.frame_scrollArea_content.children():
            if isinstance(child, QFrame):
                self.index += 1

        if self.index == 100:
            QMessageBox.critical(self, 'Ders kotası doldu', 'En fazla 100 ders ekleyebilirsiniz!')
            return None


        self.frame_name = f"lesson_frame_{self.index}"
        self.button_sil_name = f"button_sil_{self.index}"
        self.lesson_score_name = f"lesson_score_{self.index}"
        self.lesson_credit_name = f"lesson_credit_{self.index}"
        self.lesson_name = f"lesson_name_{self.index}"


        self.lesson_frame_ex = QtWidgets.QFrame(self.ui.frame_scrollArea_content)
        self.lesson_frame_ex.setMinimumSize(QtCore.QSize(600, 50))
        self.lesson_frame_ex.setMaximumSize(QtCore.QSize(16777215, 50))
        self.lesson_frame_ex.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lesson_frame_ex.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lesson_frame_ex.setObjectName(self.frame_name)
        self.layout_ders_ex = QtWidgets.QHBoxLayout(self.lesson_frame_ex)
        self.layout_ders_ex.setContentsMargins(0, 0, 0, 0)
        self.layout_ders_ex.setSpacing(20)
        self.layout_ders_ex.setObjectName("layout_ders_ex")
        self.edit_lesson_name_ex = QtWidgets.QLineEdit(self.lesson_frame_ex)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edit_lesson_name_ex.sizePolicy().hasHeightForWidth())
        self.edit_lesson_name_ex.setSizePolicy(sizePolicy)
        self.edit_lesson_name_ex.setMinimumSize(QtCore.QSize(0, 35))
        self.edit_lesson_name_ex.setMaximumSize(QtCore.QSize(9999, 16777215))
        self.edit_lesson_name_ex.setPlaceholderText("")
        self.edit_lesson_name_ex.setObjectName(self.lesson_name)
        self.layout_ders_ex.addWidget(self.edit_lesson_name_ex)
        self.combo_lesson_score_ex = QtWidgets.QComboBox(self.lesson_frame_ex)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_lesson_score_ex.sizePolicy().hasHeightForWidth())
        self.combo_lesson_score_ex.setSizePolicy(sizePolicy)
        self.combo_lesson_score_ex.setMinimumSize(QtCore.QSize(100, 35))
        self.combo_lesson_score_ex.setMaximumSize(QtCore.QSize(100, 16777215))
        self.combo_lesson_score_ex.setObjectName(self.lesson_score_name)
        self.combo_lesson_score_ex.addItem("")
        self.combo_lesson_score_ex.addItem("")
        self.combo_lesson_score_ex.addItem("")
        self.combo_lesson_score_ex.addItem("")
        self.combo_lesson_score_ex.addItem("")
        self.combo_lesson_score_ex.addItem("")
        self.combo_lesson_score_ex.addItem("")
        self.combo_lesson_score_ex.addItem("")
        self.combo_lesson_score_ex.addItem("")
        self.layout_ders_ex.addWidget(self.combo_lesson_score_ex)
        self.spinbox_lesson_credit_ex = QtWidgets.QSpinBox(self.lesson_frame_ex)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinbox_lesson_credit_ex.sizePolicy().hasHeightForWidth())
        self.spinbox_lesson_credit_ex.setSizePolicy(sizePolicy)
        self.spinbox_lesson_credit_ex.setMinimumSize(QtCore.QSize(100, 35))
        self.spinbox_lesson_credit_ex.setMaximumSize(QtCore.QSize(100, 16777215))
        self.spinbox_lesson_credit_ex.setMaximum(9)
        self.spinbox_lesson_credit_ex.setObjectName(self.lesson_credit_name)
        self.layout_ders_ex.addWidget(self.spinbox_lesson_credit_ex)
        self.button_sil_ex = QtWidgets.QPushButton(self.lesson_frame_ex)
        self.button_sil_ex.setMinimumSize(QtCore.QSize(35, 35))
        self.button_sil_ex.setMaximumSize(QtCore.QSize(35, 35))
        self.button_sil_ex.setStyleSheet("")
        self.button_sil_ex.setObjectName(self.button_sil_name)

        self.button_sil_ex.clicked.connect(self.func_sil)

        self.layout_ders_ex.addWidget(self.button_sil_ex)
        self.layout_ders_ex.setStretch(0, 7)
        self.layout_ders_ex.setStretch(1, 1)
        self.layout_ders_ex.setStretch(2, 1)
        self.layout_ders_ex.setStretch(3, 1)
        # -------------------------------------------------------------
        self.layout_total_index = self.ui.layout_scrollArea_content.count()
        self.ui.layout_scrollArea_content.insertWidget(self.layout_total_index - 1, self.lesson_frame_ex)
        # --------------------------------------------------------------

        _translate = QtCore.QCoreApplication.translate
        self.combo_lesson_score_ex.setItemText(0, _translate("MainWindow", "AA"))
        self.combo_lesson_score_ex.setItemText(1, _translate("MainWindow", "BA"))
        self.combo_lesson_score_ex.setItemText(2, _translate("MainWindow", "BB"))
        self.combo_lesson_score_ex.setItemText(3, _translate("MainWindow", "CB"))
        self.combo_lesson_score_ex.setItemText(4, _translate("MainWindow", "CC"))
        self.combo_lesson_score_ex.setItemText(5, _translate("MainWindow", "DC"))
        self.combo_lesson_score_ex.setItemText(6, _translate("MainWindow", "DD"))
        self.combo_lesson_score_ex.setItemText(7, _translate("MainWindow", "FD"))
        self.combo_lesson_score_ex.setItemText(8, _translate("MainWindow", "FF"))
        self.button_sil_ex.setText(_translate("MainWindow", "Sil"))

    def func_sil(self):
        self.button = self.sender()
        self.button_object_name = self.button.objectName()
        self.index = self.button_object_name[-1]
        self.frame_object_name = f"lesson_frame_{self.index}"
        self.frame = self.findChild(QFrame, self.frame_object_name)
        self.ui.layout_scrollArea_content.removeWidget(self.frame)
        self.frame.setParent(None)


    def func_tumunu_sil(self):
        self.layout_sac = self.ui.layout_scrollArea_content 
        self.frame_count = self.ui.layout_scrollArea_content.count()

        if self.frame_count > 1:
            for i in range(self.frame_count - 1, 0, -1):
                frame_item = self.layout_sac.itemAt(i)
                if frame_item and frame_item.widget() and isinstance(frame_item.widget(), QFrame):
                    self.frame = frame_item.widget()
                    self.layout_sac.removeWidget(self.frame)
                    self.frame.setParent(None)

    def func_hesapla(self):
        self.input_agno = self.ui.spinbox_input_agno.value()
        self.input_kredi = self.ui.spinbox_input_kredi.value()
        self.mevcut_agno_weight = self.input_agno * self.input_kredi


        self.index = -1
        for child in self.ui.frame_scrollArea_content.children():
            if isinstance(child, QFrame):
                self.index += 1

        if self.index > 0:
            self.df_dersler = pd.DataFrame() 
            for i in range(0, self.index):
                score = self.findChild(QComboBox, f"lesson_score_{i}")
                credit = self.findChild(QSpinBox, f"lesson_credit_{i}")

                dic_dersler = {
                    'score': score.currentText(),
                    'credit': credit.value(),
                }

                self.df_dersler = self.df_dersler.append(dic_dersler, ignore_index=True)

            self.df_dersler['score_numeric'] = self.df_dersler['score'].replace({'AA': 4, 'BA': 3.5, 'BB': 3, 'CB': 2.5, 'CC': 2, 'DC': 1.5, 'DD': 1, 'FD': 0.5, 'FF': 0})
            self.df_dersler['weighted score'] = self.df_dersler['score_numeric'] * self.df_dersler['credit']
            self.total_agno_weighted_score = self.mevcut_agno_weight + self.df_dersler['weighted score'].sum()
            self.calculated_agno = self.total_agno_weighted_score / (self.input_kredi + self.df_dersler['credit'].sum())
            self.calculated_agno = "{:.2f}".format(self.calculated_agno)
            self.ui.text_agno_ekran.setText(str(self.calculated_agno))
            
        


    def read_database(self):
        self.df1 = pd.read_csv('db1.csv')
        if len(self.df1) > 0:
            self.cc = self.df1.iloc[0,0]
            self.ca = self.df1.iloc[0,1]
            self.ui.spinbox_input_kredi.setValue(self.cc)
            self.ui.spinbox_input_agno.setValue(self.ca)


        self.df2 = pd.read_csv('db2.csv')
        self.index = len(self.df2)
        if self.index > 0:
            for row in range(0, self.index):
                # 1. Öncelikle o row'u ekleyelim
                self.func_ders_ekle()

                # 2. Row'a yazılacak değerleri database'den çek 
                self.le = self.df2.iloc[row,0]
                self.sc = self.df2.iloc[row,1]
                self.cr = self.df2.iloc[row,2]

                # 3. Row'un her columns'unu bul ve gerekli değeri ata
                self.lesson_object_name = f"lesson_name_{row}"
                self.lesson = self.findChild(QLineEdit, self.lesson_object_name).setText(self.le)

                self.score_object_name = f"lesson_score_{row}"
                self.score = self.findChild(QComboBox, self.score_object_name)
                self.index_score_item = self.score.findText(self.sc)
                if self.index_score_item != -1:
                    self.score.setCurrentIndex(self.index_score_item)

                self.credit_object_name = f"lesson_credit_{row}"
                self.credit = self.findChild(QSpinBox, self.credit_object_name).setValue(self.cr)







def runApp():
    app = QApplication([])
    newWindow = AppWindow()
    newWindow.show()
    app.exec_()
runApp()