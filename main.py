''' Необходимые модули '''
import json
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QHBoxLayout,
                             QInputDialog, QLabel, QLineEdit, QListWidget,
                             QPushButton, QTextEdit, QVBoxLayout, QWidget)
from qt_material import apply_stylesheet


''' Заметка в json '''
notes = {
    'Добро пожаловать': {
        'текст': 'Это самое лучшее приложение для заметок в мире!',
        'теги': ['добро', 'инструкция']
    }
}

# если заметки не существует
if not os.path.exists('notes_data.json'):
    # сохраняем стартовую заметку в новый созданный json файл
    with open('notes_data.json', 'w', encoding='utf-8') as file:
        json.dump(notes, file, sort_keys=True, ensure_ascii=False, indent=4)

''' Приложение '''
# объект приложения
app = QApplication([])
apply_stylesheet(app, theme='light_blue.xml') # тема для приложения

''' Интерфейс приложения '''
# объект окна
window = QWidget()
# задаем параметров
window.setWindowTitle('Умные заметки')
window.resize(900, 600)

# # виджеты окна приложения

# окно текста заметки
field_text = QTextEdit()

# окно списка заметок
list_notes = QListWidget()
list_notes_label = QLabel('Умные заметки')

# кнопки для заметок
btn_create_note = QPushButton('Создать заметку')
btn_delete_note = QPushButton('Удалить заметку')
btn_save_note = QPushButton('Сохранить заметку')

# окно списка тегов заметки
list_tags = QListWidget()
list_tags_label = QLabel('Список тегов')

# окно ввода тега
field_tag = QLineEdit()
field_tag.setPlaceholderText('Введите тег...')

# кнопки для тегов
btn_add_tag = QPushButton('Добавить к заметке')
btn_delete_tag = QPushButton('Открепить от заметки')
btn_search_tag = QPushButton('Искать заметки по тегу')

# # размещение виджетов по лэйаутам

# первый "столбец"-лэйаут
col1 = QVBoxLayout()
col1.addWidget(field_text)

# второй "столбец"-лэйаут
col2 = QVBoxLayout()
col2.addWidget(list_notes_label) # надпись
col2.addWidget(list_notes)       # список заметок

# кнопки для работы с заметками
row1 = QHBoxLayout()             # 1 "линия"-лэйаут с кнопками
row1.addWidget(btn_create_note)  # кнопка "Создать"
row1.addWidget(btn_delete_note)  # кнопка "Удалить"
row2 = QHBoxLayout()             # 2 "линия"-лэйаут с кнопками
row2.addWidget(btn_save_note)    # кнопка "Сохранить"

# добавляем обе "линии"-лэйаута с кнопками
# на 2 столбец
col2.addLayout(row1)
col2.addLayout(row2)

# добавляем на 2 "столбец"-лэйаут
# список тегов и поле для ввода тега
col2.addWidget(list_tags_label)
col2.addWidget(list_tags)
col2.addWidget(field_tag)

# кнопки для работы с тегами
row3 = QHBoxLayout()             # 3 "линия"-лэйаут с кнопками
row3.addWidget(btn_add_tag)      # кнопка "Добавить тег"
row3.addWidget(btn_delete_tag)   # кнопка "Удалить тег"
row4 = QHBoxLayout()             # 4 "линия"-лэйаут с кнопками
row4.addWidget(btn_search_tag)   # кнопка "Искать по тегу"

# добавляем обе "линии"-лэйаута с кнопками
# на 2 столбец
col2.addLayout(row3)
col2.addLayout(row4)

# главная "линия"-лэйаут окна
# на неё добавляются 2 "столбца"-лэйаута
layout_notes = QHBoxLayout()
layout_notes.addLayout(col1, stretch=2)
layout_notes.addLayout(col2, stretch=1)

# прикрепляем линию на окно
window.setLayout(layout_notes)

''' Функционал приложения '''

# функция для отображения заметки
def show_note():
    key = list_notes.selectedItems()[0].text() # вытаскиваем название выбранной заметки
    field_text.setText(notes[key]['текст'])    # устанавливаем в поле текст этой заметки
    list_tags.clear()                          # очищаем список тегов
    list_tags.addItems(notes[key]['теги'])     # добавляем теги этой заметки в список тегов

# функция для создания заметки
def add_note():
    # вызываем окно для ввода названия новой заметки
    note_name, ok = QInputDialog.getText(window, 'Добавить заметку', 'Название заметки:')
    # если нажато "OK" и название новой заметки не пустое
    if ok and note_name != '':
        notes[note_name] = {'текст': '', 'теги': []} # добавляем пустую заметку в словарь
        list_notes.addItem(note_name)                # добавляем название заметки в список заметок

# функция для сохранения заметки
def save_note():
    # если выбрана какая-то заметка
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()      # вытаскиваем название выбранной заметки
        notes[key]['текст'] = field_text.toPlainText()  # сохраняем текст из поля в нашу заметку
        # и записываем словарь notes с заметками в json файл
        with open('notes_data.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False, indent=4)
        print(notes) # и печатаем словарь на экран
    # если НЕ выбрана заметка
    else:
        print("Заметка для сохранения не выбрана!")

# функция для удаления заметки
def del_note():
    # если выбрана какая-то заметка
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()  # вытаскиваем название выбранной заметки
        del notes[key]                              # удаляем заметку с этим названием из словаря
        list_notes.clear()                          # очищаем список заметок
        list_tags.clear()                           # очищаем список тегов
        field_text.clear()                          # очищаем поле для текста заметки
        list_notes.addItems(notes)                  # добавляем названия заметок в список заметок
        # и записываем словарь notes с заметками в json файл
        with open('notes_data.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False, indent=4)
        print(notes) # и печатаем словарь на экран
    # если НЕ выбрана заметка
    else:
        print('Заметка для удаления не выбрана!')

''' Функции для работы с тегами заметки'''
# функция для добавления тега
def add_tag():
    # если выбрана какая-то заметка
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()  # вытаскиваем название выбранной заметки
        tag = field_tag.text()                      # вытаскиваем введенный тег
        # если введеного тега нет в тегах выбранной заметки и он не пустой
        if not tag in notes[key]['теги'] and tag != '':
            notes[key]['теги'].append(tag) # добавляем этот тег в теги заметки
            list_tags.addItem(tag)         # добавляем его в список тегов
            field_tag.clear()              # очищаем поле для ввода тега
            # и записываем словарь notes с заметками в json файл
            with open('notes_data.json', 'w', encoding='utf-8') as file:
                json.dump(notes, file, sort_keys=True, ensure_ascii=False, indent=4)
            print(notes) # и печатаем словарь на экран
    # если НЕ выбрана заметка
    else:
        print('Заметка для добавления тега не выбрана')

# функция для открепления тега
def del_tag():
    # если выбрана какая-то заметка
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()  # вытаскиваем название выбранной заметки
        tag = list_tags.selectedItems()[0].text()   # вытаскиваем выбранный тег
        notes[key]['теги'].remove(tag)              # удаляем тег из тегов заметки
        list_tags.clear()                           # очищаем список тегов
        list_tags.addItems(notes[key]['теги'])      # и добавляем в него теги заметки обратно
        # и записываем словарь notes с заметками в json файл
        with open('notes_data.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False, indent=4)
        print(notes) # и печатаем словарь на экран
    # если выбрана какая-то заметка
    else:
        print('Тег для удаления не выбран!')

# функция для поиска по тегу
def search_tag():
    tag = field_tag.text() # вытаскиваем введенный тег

    # если текст на кнопке "Искать заметки по тегу"
    if btn_search_tag.text() == "Искать заметки по тегу":
        print(tag) # печатаем введенный тег
        notes_filtered = {} # словарь с отфильтрованными заметками с введенным тегом

        # проходимся по всем заметкам в словаре notes
        for note in notes:
            # если введенный тег есть в тегах какой-то заметки
            if tag in notes[note]['теги']:
                # добавляем эту заметку в словарь отфильтрованных
                notes_filtered[note] = notes[note]
    
        btn_search_tag.setText('Сбросить поиск') # устанавливаем текст на кнопке "Сбросить поиск"
        list_notes.clear()                       # очищаем список заметок
        list_tags.clear()                        # очищаем список тегов
        list_notes.addItems(notes_filtered)      # добавляем в список заметок названия отфильтрованных
    # если текст на кнопке "Сбросить поиск"
    elif btn_search_tag.text() == "Сбросить поиск":
        field_tag.clear()   # очищаем поле для ввода тега
        list_notes.clear()  # очищаем список заметок
        list_tags.clear()   # очищаем список тегов
        list_notes.addItems(notes) # добавляем названия заметок в список заметок
        btn_search_tag.setText('Искать заметки по тегу') # устанавливаем текст на кнопке "Искать заметки по тегу"
    # в противном случае
    else:
        # ничего не делаем
        pass

# # подключение функций к кнопками
# работа с заметками
list_notes.itemClicked.connect(show_note) # при нажатии на название заметки показываем её
btn_create_note.clicked.connect(add_note) # создание заметки
btn_save_note.clicked.connect(save_note)  # сохранение заметки
btn_delete_note.clicked.connect(del_note) # удаление заметки
# работа с тегами
btn_add_tag.clicked.connect(add_tag)      # добавление тега
btn_delete_tag.clicked.connect(del_tag)   # удаление тега
btn_search_tag.clicked.connect(search_tag)# поиск по тегу

# считываем файл с заметками и запоминаем в словарь notes
with open('notes_data.json', 'r', encoding='utf-8') as file:
    notes = json.load(file)
# добавляем названия заметок в список заметок
list_notes.addItems(notes)

# показываем окно
window.show()

# запускаем приложение
app.exec_()