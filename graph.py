# Подключаем всё для создания графического интерфейса
import sys
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QApplication, QFileDialog, QMessageBox
)
from PyQt6.QtCore import QVariant # аналог return None
# from main_window import Ui_MainWindow # подключаем сконвертированные ui-файлы
# from additional_window import Ui_Form
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIcon

# Построение графиков, вычисления
import numpy as np
import sympy
import matplotlib.pyplot as plt
from random import choice # выбор цветов из готового набора

# ЗАГРУЖАЕМ СТИЛИ И HTML
MAIN_WINDOW_LIGHT_STYLES = '''
/* Стиль для главного окна */
QMainWindow {
    background-color: #EEE;
}

/* Стиль для текстового поля */
QPlainTextEdit {
    background-color: #FFF;
    color: #000;
    border: 2px solid #767;
    font-size: 25.5px;
    font-family: "Arial", sans-serif;
}

/* Стиль для всего меню-бара */
QMenuBar {
    background-color: #FFF;
    color: #000;
}

/* Стиль для отдельного пункта меню (Файл, Правка...) */
QMenuBar::item {
    background-color: transparent;
}

/* Стиль для пункта меню при его выборе */
QMenuBar::item:selected {
    background-color: #EEE;
    border: 1px solid #EEE;
    border-radius: 4px;
}

/* Стиль для выпадающего меню */
QMenu {
    background-color: #FFF;
    color: #000;
    border: 1px solid #767;
}

/* Стиль для пунктов в выпадающем меню при наведении */
QMenu::item:selected {
    background-color: #EEE;
    border: 1px solid #EEE;
    border-radius: 4px;
}

/* Стиль для кнопок */
QPushButton {
    background-color: #FFF;
    color: #000;
    border: 1px solid #DDD;
    border-radius: 5px;
    padding: 10px 20px;
    font-size: 11.6pt;
    font-family: "Arial", sans-serif;
}

/* Стиль для кнопок при наведении мыши */
QPushButton:hover {
    border: 2px solid #3498db;
    border-radius: 10px;
}

/* Стиль для кнопок при клике мышки */
QPushButton:pressed {
    border: 2px solid #156AAB;
    border-radius: 10px;
}
'''

MAIN_WINDOW_DARK_STYLES = '''
/* Стиль для главного окна */
QMainWindow {
    background-color: #2b2b2b;
}

/* Стиль для текстового поля */
QPlainTextEdit {
    background-color: #3c3f41;
    color: #a9b7c6;
    border: 2px solid #555;
    font-size: 25.5px;
    font-family: "Arial", sans-serif;
}

/* Стиль для всего меню-бара */
QMenuBar {
    background-color: #3c3f41;
    color: #a9b7c6;
}

/* Стиль для отдельного пункта меню (Файл, Правка...) */
QMenuBar::item {
    background-color: transparent;
}

/* Стиль для пункта меню при его выборе */
QMenuBar::item:selected {
    border: 1px solid #555;
    border-radius: 4px;
    background-color: #555;
}

/* Стиль для выпадающего меню */
QMenu {
    background-color: #3c3f41;
    color: #a9b7c6;
    border: 1px solid #555;
}

/* Стиль для пунктов в выпадающем меню при наведении */
QMenu::item:selected {
    background-color: #555;
    border: 1px, solid, #555;
    border-radius: 4px;
}

/* Стиль для кнопок */
QPushButton {
    background-color: #3c3f41;
    color: #a9b7c6;
    border: 1px solid #555;
    border-radius: 5px;
    padding: 10px 20px;
    font-size: 11.6pt;
    font-family: "Arial", sans-serif;
}

/* Стиль для кнопок при наведении мыши */
QPushButton:hover {
    border: 2px solid #3498db;
    border-radius: 10px;
}

/* Стиль для кнопок при клике мышки */
QPushButton:pressed {
    border: 2px solid #156AAB;
    border-radius: 10px;
}
'''

SYNTAX_RULES_HTML_LIGHT = '''
<body style="font-family: Verdana, sans-serif; background-color: #FFF; color: #000;">
    <h1>Обозначения переменных</h1>
    <p style="font-size: 10.5pt;">Разрешены только x и y. Другие имена переменных не допускаются.</p>
    <h1>Арифметические операции</h1>
    <ul style="font-size: 10.5pt;">
        <li>Всегда с двух сторон окружаются пробелами: +, -, =.</li>
        <li>В свою очередь, * (умножение), ** (возведение в степень) и / (деление) не окружаются пробелами, а ставятся вплотную к символам.</li>
        <li>Дробная черта не предусмотрена. Перед делением одного выражения на другое, необходимо вплотную окружить их круглыми скобками: ().</li>
        <li>При возведении одного выражения в степень другого выражения они оба окружаются круглыми скобками ().</li>
    </ul>
    <h1>Модули, корни n-ной степени, тригонометрические функции, логарифмы. Число пи и число Эйлера</h1>
    <ul style="font-size: 10.5pt;">
        <li>Модуль выражения A обозначается как abs(A).</li>
        <li>Чтобы взять корень n-ной степени из выражения или некого числа A, необходимо возвести его в степень (1/n), то есть это равносильно A**(1/n).</li>
        <li>Функции sin(x), cos(x), tg(x), ctg(x) обозначаются как sin(x), cos(x), tan(x) и cot(x) соответственно.</li>
        <li>Логарифм b по основанию a обозначается как log(b, a).</li>
        <li>Число пи и число Эйлера обозначаются как pi и E соответственно.</li>
    </ul>
    <h1>Примеры</h1>
    <ul style="font-size: 10.5pt;">
        <li>y = x**2</li>
        <li>x = y**0.5</li>
        <li>y = x**(1/3)</li>
        <li>y = x**4 + 10*x**3 + 5*x**2 + 10*x + 1</li>
        <li>x**2 + y**2 = 36</li>
        <li>4*x**2 + y**2 = 625**(1/2)</li>
        <li>abs(x) + abs(y) = 1</li>
        <li>abs(x - 5)/5 + abs(y - 5)/5 = 1</li>
        <li>y = 1/(x + 2) + 5</li>
        <li>y = (3*x + 5)/(9*x + 3)</li>
        <li>y = sin(x)/cos(x)</li>
        <li>abs(y) = sin(x/2) + 0.3</li>
        <li>y = 2**(x - 1)</li>
        <li>y**(x**2 - 5*x + 6) = x**(y**2 - 5*x + 6)</li>
        <li>y = E**x</li>
        <li>y = sin(x + pi/2)</li>
    </ul>
</body>
'''

SYNTAX_RULES_HTML_DARK = '''
<body style="font-family: Verdana, sans-serif; background-color: #3c3f41; color: #FFF;">
    <h1>Обозначения переменных</h1>
    <p style="font-size: 10.5pt;">Разрешены только x и y. Другие имена переменных не допускаются.</p>
    <h1>Арифметические операции</h1>
    <ul style="font-size: 10.5pt;">
        <li>Всегда с двух сторон окружаются пробелами: +, -, =.</li>
        <li>В свою очередь, * (умножение), ** (возведение в степень) и / (деление) не окружаются пробелами, а ставятся вплотную к символам.</li>
        <li>Дробная черта не предусмотрена. Перед делением одного выражения на другое, необходимо вплотную окружить их круглыми скобками: ().</li>
        <li>При возведении одного выражения в степень другого выражения они оба окружаются круглыми скобками ().</li>
    </ul>
    <h1>Модули, корни n-ной степени, тригонометрические функции, логарифмы. Число пи и число Эйлера</h1>
    <ul style="font-size: 10.5pt;">
        <li>Модуль выражения A обозначается как abs(A).</li>
        <li>Чтобы взять корень n-ной степени из выражения или некого числа A, необходимо возвести его в степень (1/n), то есть это равносильно A**(1/n).</li>
        <li>Функции sin(x), cos(x), tg(x), ctg(x) обозначаются как sin(x), cos(x), tan(x) и cot(x) соответственно.</li>
        <li>Логарифм b по основанию a обозначается как log(b, a).</li>
        <li>Число пи и число Эйлера обозначаются как pi и E соответственно.</li>
    </ul>
    <h1>Примеры</h1>
    <ul style="font-size: 10.5pt;">
        <li>y = x**2</li>
        <li>x = y**0.5</li>
        <li>y = x**(1/3)</li>
        <li>y = x**4 + 10*x**3 + 5*x**2 + 10*x + 1</li>
        <li>x**2 + y**2 = 36</li>
        <li>4*x**2 + y**2 = 625**(1/2)</li>
        <li>abs(x) + abs(y) = 1</li>
        <li>abs(x - 5)/5 + abs(y - 5)/5 = 1</li>
        <li>y = 1/(x + 2) + 5</li>
        <li>y = (3*x + 5)/(9*x + 3)</li>
        <li>y = sin(x)/cos(x)</li>
        <li>abs(y) = sin(x/2) + 0.3</li>
        <li>y = 2**(x - 1)</li>
        <li>y**(x**2 - 5*x + 6) = x**(y**2 - 5*x + 6)</li>
        <li>y = E**x</li>
        <li>y = sin(x + pi/2)</li>
    </ul>
</body>
'''
FILE_RULES_HTML_LIGHT = '''
<body style="font-family: Verdana, sans-serif; background-color: #FFF; color: #000;">
    <h1>Правила именования сохраняемых файлов</h1>
    <ul style="font-size: 10.5pt;">
        <li>Приложение поддерживает и работает только с файлами формата ".txt".</li>
        <li>Запрещённые символы: '/', '|', '\', "*",  ";", ":", "&", "!", "?", '"', "'", "[", "]",
            "&gt;", "&lt;", "=", "#", "%", "$", "~", "`" (апостроф), ",", "{", "}", "(", ")", " " (пробелы).</li>
        <li>Также запрещено использование "." (точек) в названиях файлов. Точка ставится только перед расширением .txt сохраняемого файла.</li>
        <li>Имя файла не может быть пустым. То есть файл не может быть сохранён, если перед .txt ничего нет.</li>
    </ul>
</body>
'''
FILE_RULES_HTML_DARK = '''
<body style="font-family: Verdana, sans-serif; background-color: #3c3f41; color: #FFF;">
    <h1>Правила именования сохраняемых файлов</h1>
    <ul style="font-size: 10.5pt;">
        <li>Приложение поддерживает и работает только с файлами формата ".txt".</li>
        <li>Запрещённые символы: '/', '|', '\', "*",  ";", ":", "&", "!", "?", '"', "'", "[", "]",
            "&gt;", "&lt;", "=", "#", "%", "$", "~", "`" (апостроф), ",", "{", "}", "(", ")", " " (пробелы).</li>
        <li>Также запрещено использование "." (точек) в названиях файлов. Точка ставится только перед расширением .txt сохраняемого файла.</li>
        <li>Имя файла не может быть пустым. То есть файл не может быть сохранён, если перед .txt ничего нет.</li>
    </ul>
</body>
'''


# Переменные в качестве символов sympy создаются единожды, обозначим их константами
X, Y = sympy.symbols("x y")
FOR_CONVERTATION = {"x": X, "y": Y}
x_vals, y_vals = np.linspace(-300, 300, 4001), np.linspace(-300, 300, 4001)
OX, OY = np.meshgrid(x_vals, y_vals) # создаём единую матрицу координат x и y

# Цвета для графиков в удобоваримом для matplotlib формате
GRAPH_COLORS = [(0.376, 1.0, 0.204), (0.396, 0.047, 0.961), (0.318, 0.886, 0.988), (0.976, 0.675, 0.106),
                (1.0, 0.988, 0.29), (0.925, 0.118, 0.09), (0.925, 0.09, 0.898), (0.282, 0.612, 0.224),
                (0.078, 0.38, 0.31), (0.361, 0.224, 0.612), (0.31, 0.078, 0.38), (0.98, 0.514, 0.506),
                (0.0, 0.298, 0.651), (0.082, 0.482, 0.58), (0.682, 0.518, 0.357),
                (0.816, 0.267, 0.369), (0.882, 0.91, 0.427), (0.239, 0.392, 0.541), (0.078, 0.259, 0.396)]

# Недопустимые имена файлов
RESTRICTED_SYMBOLS = ['/', '|', '\\', "*",  ";", ":", "&", "!", "?", '"', "'", "[", "]",
                      ">", "<", "=", "#", "%", "$", "~", "`", ",", "{", "}", "(", ")", " "]


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 500)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.inputList = QtWidgets.QPlainTextEdit(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputList.sizePolicy().hasHeightForWidth())
        self.inputList.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.inputList.setFont(font)
        self.inputList.setPlainText("")
        self.inputList.setObjectName("inputList")
        self.gridLayout.addWidget(self.inputList, 0, 0, 1, 1)
        self.plotButton = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.plotButton.sizePolicy().hasHeightForWidth())
        self.plotButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.plotButton.setFont(font)
        self.plotButton.setObjectName("plotButton")
        self.gridLayout.addWidget(self.plotButton, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 26))
        self.menubar.setObjectName("menubar")
        self.helpMenu = QtWidgets.QMenu(parent=self.menubar)
        self.helpMenu.setObjectName("helpMenu")
        self.fileMenu = QtWidgets.QMenu(parent=self.menubar)
        self.fileMenu.setObjectName("fileMenu")
        self.menu = QtWidgets.QMenu(parent=self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.syntax_rules = QtGui.QAction(parent=MainWindow)
        self.syntax_rules.setObjectName("syntax_rules")
        self.loadAction = QtGui.QAction(parent=MainWindow)
        self.loadAction.setObjectName("loadAction")
        self.saveAction = QtGui.QAction(parent=MainWindow)
        self.saveAction.setObjectName("saveAction")
        self.exportAction = QtGui.QAction(parent=MainWindow)
        self.exportAction.setObjectName("exportAction")
        self.newFileAction = QtGui.QAction(parent=MainWindow)
        self.newFileAction.setObjectName("newFileAction")
        self.file_rules = QtGui.QAction(parent=MainWindow)
        self.file_rules.setObjectName("file_rules")
        self.lightTheme = QtGui.QAction(parent=MainWindow)
        self.lightTheme.setObjectName("lightTheme")
        self.darkTheme = QtGui.QAction(parent=MainWindow)
        self.darkTheme.setObjectName("darkTheme")
        self.helpMenu.addAction(self.syntax_rules)
        self.helpMenu.addAction(self.file_rules)
        self.fileMenu.addAction(self.newFileAction)
        self.fileMenu.addAction(self.loadAction)
        self.fileMenu.addAction(self.saveAction)
        self.menu.addAction(self.lightTheme)
        self.menu.addAction(self.darkTheme)
        self.menubar.addAction(self.helpMenu.menuAction())
        self.menubar.addAction(self.fileMenu.menuAction())
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Graph"))
        self.plotButton.setText(_translate("MainWindow", "Построить"))
        self.helpMenu.setTitle(_translate("MainWindow", "Помощь"))
        self.fileMenu.setTitle(_translate("MainWindow", "Файл"))
        self.menu.setTitle(_translate("MainWindow", "Оформление"))
        self.syntax_rules.setText(_translate("MainWindow", "Правила записи функций и множеств точек"))
        self.loadAction.setText(_translate("MainWindow", "Загрузить файл"))
        self.saveAction.setText(_translate("MainWindow", "Сохранить файл"))
        self.exportAction.setText(_translate("MainWindow", "Экспорт в формате .png"))
        self.newFileAction.setText(_translate("MainWindow", "Новый файл"))
        self.file_rules.setText(_translate("MainWindow", "Правила записи имён файлов"))
        self.lightTheme.setText(_translate("MainWindow", "Светлая тема"))
        self.darkTheme.setText(_translate("MainWindow", "Тёмная тема"))


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(496, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.styledText = QtWidgets.QTextBrowser(parent=Form)
        self.styledText.setMaximumSize(QtCore.QSize(475, 16777215))
        self.styledText.setObjectName("styledText")
        self.gridLayout.addWidget(self.styledText, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Правила записи"))
        self.styledText.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))


class SyntaxRulesWindow(QWidget, Ui_Form):
    '''Окно, вызываемое пунктом "Правила записи функций" в меню "Помощь" '''
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(500, 500)
        self.styledText.setHtml(SYNTAX_RULES_HTML_LIGHT)
        self.setWindowIcon(QIcon("min.png"))


class FileRulesWindow(QWidget, Ui_Form):
    '''Окно, вызываемое пунктом "Правила записи имён файлов" в меню "Помощь" '''
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(500, 500)
        self.styledText.setHtml(FILE_RULES_HTML_LIGHT)
        self.setWindowIcon(QIcon("min.png"))


class MainWindow(QMainWindow, Ui_MainWindow):
    '''Главное окно приложения'''
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet(MAIN_WINDOW_LIGHT_STYLES)

        self.current_file_name = "" # Имя текущего файла для отображения в заголовке окна
        self.current_theme = "light" # Текущая установленная тема
        self.setWindowTitle("Graph; открыт новый файл.")
        self.setWindowIcon(QIcon("min.png"))

        # Подключаем кнопки и действия
        self.newFileAction.triggered.connect(self.new_file)
        self.loadAction.triggered.connect(self.load_file)
        self.saveAction.triggered.connect(self.save_file)
        self.plotButton.clicked.connect(self.plotting)
        self.lightTheme.triggered.connect(self.set_light_theme)
        self.darkTheme.triggered.connect(self.set_dark_theme)

        # Вызов других форм и всплывающих окон
        self.syntax_rules_window = SyntaxRulesWindow()
        self.syntax_rules.triggered.connect(self.show_syntax_rules)

        self.file_rules_window = FileRulesWindow()
        self.file_rules.triggered.connect(self.show_file_rules)

        self.no_file_name = QMessageBox(self)
        self.no_file_name.setInformativeText("Файл не был выбран.")
        self.no_file_name.addButton("Пропустить", QMessageBox.ButtonRole.RejectRole)
        self.no_file_name.setIcon(QMessageBox.Icon.Critical)
        self.incorrect_file_name = QMessageBox(self)
        self.incorrect_file_name.setInformativeText("Некорректное имя файла.")
        self.incorrect_file_name.addButton("Пропустить", QMessageBox.ButtonRole.RejectRole)
        self.incorrect_file_name.setIcon(QMessageBox.Icon.Critical)


    def new_file(self):
        if self.current_file_name:
            self.current_file_name = ""
            self.setWindowTitle("Graph; открыт новый файл.")
            self.inputList.setPlainText("")

    def load_file(self):
        loaded_file_name = QFileDialog.getOpenFileName(self, "Выберите файл.", "", "Текст (*.txt)")[0]
        if not loaded_file_name:
            return QVariant()
        with open(loaded_file_name, "r", encoding="utf8") as file_to_load:
            self.inputList.setPlainText(file_to_load.read())
            self.current_file_name = loaded_file_name.split("/")[-1]
            self.setWindowTitle("Graph; открыт " + self.current_file_name)

    def save_file(self):
        suggested_name = ".txt"
        if self.current_file_name:
            # Если был открытый файл, предлагаем его сохранить
            suggested_name = self.current_file_name
        saved_file_name = QFileDialog.getSaveFileName(self, "", suggested_name, "Текст (*.txt)")[0]
        short_sfile_name = saved_file_name.split("/")[-1]
        sfile_type = short_sfile_name.split(".")[-1]
        if not saved_file_name:
            # Файл не был выбран
            self.no_file_name.exec()
            return QVariant()
        if any([i in short_sfile_name for i in RESTRICTED_SYMBOLS]) or\
            sfile_type != "txt" or short_sfile_name.count(".") > 1 or len(short_sfile_name) < 5:
            # 1) Проверка на запрещённые для имён файлов символы в ОС
            # 2) Проверка файла на правильный тип .txt
            # 3) Проверка на единственную точку и непустую часть имени без расширения
            self.incorrect_file_name.exec()
            return QVariant()
        with open(saved_file_name, "w", encoding="utf8") as file_to_save:
            for string in self.inputList.toPlainText().split("\n"):
                print(string, file=file_to_save)
            self.current_file_name = short_sfile_name
            self.setWindowTitle("Graph; открыт " + self.current_file_name)

    def set_light_theme(self):
        if self.current_theme == "dark":
            self.current_theme = "light"
            self.setStyleSheet(MAIN_WINDOW_LIGHT_STYLES)
            self.syntax_rules_window.setStyleSheet('''
            QWidget {
                background-color: #FFF;
            }
            ''')
            self.syntax_rules_window.styledText.setHtml(SYNTAX_RULES_HTML_LIGHT)
            self.file_rules_window.setStyleSheet('''
            QWidget {
                background-color: #FFF;
            }
            ''')
            self.file_rules_window.styledText.setHtml(FILE_RULES_HTML_LIGHT)

    def set_dark_theme(self):
        if self.current_theme == "light":
            self.current_theme = "dark"
            self.setStyleSheet(MAIN_WINDOW_DARK_STYLES)
            self.syntax_rules_window.setStyleSheet('''
            QWidget {
                background-color: #2b2b2b;
            }
            ''')
            self.syntax_rules_window.styledText.setHtml(SYNTAX_RULES_HTML_DARK)
            self.file_rules_window.setStyleSheet('''
            QWidget {
                background-color: #2b2b2b;
            }
            ''')
            self.file_rules_window.styledText.setHtml(FILE_RULES_HTML_DARK)

    def plotting(self):
        functions_and_sets = self.inputList.toPlainText().split("\n")

        # Если есть пустые строки, это расценивается как некорректный формат ввода
        if '' in functions_and_sets:
            return QVariant()
        
        # Заводим общий список уравнений
        equations = []
        for eq in functions_and_sets:
            sides1, sides2 = eq.split(" = ")
            sides1 = sympy.sympify(sides1, locals=FOR_CONVERTATION)
            sides2 = sympy.sympify(sides2, locals=FOR_CONVERTATION)
            equation = sides1 - sides2
            equations.append(equation)
        lambified_equations = [sympy.lambdify((X, Y), i, 'numpy') for i in equations]

        fig = plt.figure(figsize=(6, 6)) # задаём размеры отображаемого окна с графиком в дюймах
        ax = fig.add_subplot()

        if self.current_theme == "light": # для светлой темы
            ax.set_facecolor("#FFF")
            plt.axhline(y=0, color='#000', linestyle='-', alpha=0.5) # задаём стиль осям координат
            plt.axvline(x=0, color='#000', linestyle='-', alpha=0.5)
            plt.xlabel('Ox', color="#000") # подписываем оси
            plt.ylabel('Oy', color="#000")
            plt.grid(color='gray', linestyle='--', linewidth=0.5) # создаём удобную сетку для чисел на осях
            ax.tick_params(axis="x", colors="black") # раскрашиваем числа на осях
            ax.tick_params(axis="y", colors="black")
        else: # для тёмной темы
            fig.set_facecolor((0.169, 0.169, 0.169))
            ax.set_facecolor("#000")
            plt.axhline(y=0, color='#FFF', linestyle='-', alpha=0.5)
            plt.axvline(x=0, color='#FFF', linestyle='-', alpha=0.5)
            plt.xlabel('Ox', color="#FFF")
            plt.ylabel('Oy', color="#FFF")
            plt.grid(color='gray', linestyle='--', linewidth=0.5)
            ax.tick_params(axis="x", colors="white")
            ax.tick_params(axis="y", colors="white")

        plt.axis('equal') # задаём привычное 1:1 соотношение координат, чтобы не было искажений графиков
        plt.axis([-10, 10, -10, 10]) # начальный режим просмотра: от -10 до 10 по x, от -10 до 10 по y
        for x in lambified_equations:
            OZ = x(OX, OY) # рассчитываем значения каждого уравнения для матрицы
            '''
            levels вообще задаёт то, на каком 3D уровне будет строиться функция
            но у нас такие функции, что правая часть кривой f(x, y) всегда равна нулю
            в 3d пространстве этому всегда соответствует z = 0, потому мы пишем levels[0]
            можете поэкспериментировать и ввести, например, levels=5
            '''
            plt.contour(OX, OY, OZ, levels=0, colors=[choice(GRAPH_COLORS)], linewidths=2)
        plt.show()
    
    def show_syntax_rules(self):
        self.syntax_rules_window.show()

    def show_file_rules(self):
        self.file_rules_window.show()


# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())