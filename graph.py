# Подключаем всё для создания графического интерфейса
import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QApplication, QFileDialog, QMessageBox
)
from PyQt6.QtCore import QVariant # аналог return None
from PyQt6 import uic # временно, до конвертации

# Построение графиков, вычисления
import numpy as np
import sympy # !!! надо ещё тригонометрию добавить и указания к квадратному корню
import matplotlib.pyplot as plt
from random import randint as rnd

# Мелочи
import datetime as dtt
from time import sleep

# Загружаем стили
MAIN_WINDOW_LIGHT_STYLES = ''''''
RULES_WINDOW_LIGHT_STYLES = ''''''
with open("main_window.qss", "r", encoding="utf8") as style:
    MAIN_WINDOW_LIGHT_STYLES = style.read()

# Переменные в качестве символов sympy создаются единожды, обозначим их константами
X, Y = sympy.symbols("x y")
FOR_CONVERTATION = {"x": X, "y": Y}
x_vals, y_vals = np.linspace(-500, 500, 2001), np.linspace(-500, 500, 2001)
OX, OY = np.meshgrid(x_vals, y_vals) # создаём единую матрицу координат x и y

# Недопустимые имена файлов
RESTRICTED_SYMBOLS = ['/', '|', '\\', "*",  ";", ":", "&", "!", "?", '"', "'", "[", "]",
                      ">", "<", "=", "#", "%", "$", "~", "`", ",", "{", "}", "(", ")", " "]


class SyntaxRulesWindow(QWidget):
    '''Окно, вызываемое пунктом "Правила записи функций" в меню "Помощь" '''
    def __init__(self):
        super().__init__()
        uic.loadUi("rules_window.ui", self)
        self.textRules.setEnabled(False)


class MainWindow(QMainWindow):
    '''Главное окно приложения, может вызывать другие'''
    def __init__(self):
        super().__init__()
        uic.loadUi("main_window.ui", self)
        self.setStyleSheet(MAIN_WINDOW_LIGHT_STYLES)
        self.current_file_name = "" # Имя текущего файла для отображения в заголовке окна
        self.setWindowTitle("Graph; открыт новый файл.")

        # Подключаем кнопки и действия
        self.newFileAction.triggered.connect(self.new_file)
        self.loadAction.triggered.connect(self.load_file)
        self.saveAction.triggered.connect(self.save_file)
        self.plotButton.clicked.connect(self.plotting)

        # Вызов других форм и всплывающих окон
        self.syntax_rules_window = SyntaxRulesWindow()
        self.syntax_rules.triggered.connect(self.show_rules)

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

        plt.figure(figsize=(6, 6)) # задаём размеры отображаемого окна с графиком в дюймах
        plt.axhline(y=0, color='k', linestyle='-', alpha=0.5) # задаём стиль осям координат
        plt.axvline(x=0, color='k', linestyle='-', alpha=0.5)
        plt.axis('equal') # задаём привычное 1:1 соотношение координат, чтобы не было искажений графиков
        plt.xlabel('x') # подписываем оси
        plt.ylabel('y')
        for x in lambified_equations:
            OZ = x(OX, OY) # рассчитываем значения каждого уравнения для матрицы
            '''
            levels вообще задаёт то, на каком 3D уровне будет строиться функция
            но у нас такие функции, что правая часть кривой f(x, y) всегда равна нулю
            в 3d пространстве этому всегда соответствует z = 0, потому мы пишем levels[0]
            можете поэкспериментировать и ввести, например, levels=5
            '''
            plt.contour(OX, OY, OZ, levels=0, colors=[(1.0, 0, 0)], linewidths=2)
        plt.show()
    
    def show_rules(self):
        self.syntax_rules_window.show()


# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())