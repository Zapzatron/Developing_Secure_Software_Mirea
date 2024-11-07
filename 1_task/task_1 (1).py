import platform
import zipfile
from logging import fatal

import psutil
import os
import json
import string
import re
import xml
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import xmltodict


# 1. Вывести информацию в консоль о логических дисках, именах, метке тома, размере и типе файловой системы. ✅
# 2. Работа с файлами
# 2.1. Создать файл
# 2.2. Записать в файл строку, введённую пользователем
# 2.3. Прочитать файл в консоль
# 2.4. Удалить файл
# 3. Работа с форматом JSON
# 3.1. Создать файл в формате JSON в любом редакторе или с использованием данных, введенных пользователем
# 3.2. Создать новый объект. Выполнить сериализацию объекта в формате JSON и записать в файл.
# 3.3. Прочитать файл в консоль
# 3.4. Удалить файл
# 4. Работа с форматом XML
# 4.1. Создать файл в формате XML из редактора
# 4.2. Записать в файл новые данные из консоли.
# 4.3. Прочитать файл в консоль.
# 4.4. Удалить файл.
# 5. Создание zip архива, добавление туда файла, определение размера архива
# 5.1. Создать архив в формате zip
# 5.2. Добавить файл, выбранный пользователем, в архив
# 5.3. Разархивировать файл и вывести данные о нем
# 5.4. Удалить файл и архив
task_description = """\
1. Вывод информации о системе.
Работа с файлами:
2.1. Создать текстовый файл.
2.2. Записать строку в текстовый файл.
2.3. Вывести содержимое текстового файла.
2.4. Удалить текстовый файл.
Работа с форматом JSON:
3.2. Создать JSON файл с введёнными данными
3.3. Прочитать JSON файл в консоль
3.4. Удалить JSON файл.
Работа с форматом XML:
4.2. Записать данные в XML файл.
4.3. Прочитать XML файл в консоль.
4.4. Удалить XML файл.
Создание zip архива, добавление туда файла, определение размера архива:
5.1. Создать архив в формате zip
5.2. Добавить файл, выбранный пользователем, в архив
5.3. Разархивировать файл и вывести данные о нем
5.4. Удалить исходный файл и архив
Введите номер задачи: """


english_letters = string.ascii_letters

russian_letters = ''.join([chr(i) for i in range(ord('а'), ord('я')+1)]) + \
                  ''.join([chr(i) for i in range(ord('А'), ord('Я')+1)]) + 'ёЁ'

allowed_letters = english_letters + russian_letters + "123456789"


def check_symbols(input_string: str, allowed_symbols: str):
    """
    Проверка, что вся строка input_string состоит только из символов в allowed_letters_
    Регулярное выражение, которое соответствует любому символу из allowed_letters_
    """

    pattern = f"^[{re.escape(allowed_symbols)}]*$"
    match = re.match(pattern, input_string)
    # print(match)

    if not match:
        raise Exception(f"Разрешены только следующие символы: {allowed_symbols}")
    return match.string


def get_file_path(file_extension: str, input_message: str = None):
    if input_message is None:
        input_message = f"Введите имя для файла c расширением {file_extension}: "

    input_file_name = input(input_message)

    if ".." in input_file_name or "/" in input_file_name or "\\" in input_file_name:
        raise ValueError("Имя файла не должно содержать: '..', '/', '\\'")

    input_file_name = check_symbols(input_file_name, allowed_letters)
    input_file_name = input_file_name + file_extension
    # print(input_file_name)
    temp_file_path = os.path.join(os.getcwd(), input_file_name)
    # print(temp_file_path)
    return temp_file_path


def get_file_with_value_error(file_extension: str, input_message: str = None):
    try:
        return False, get_file_path(file_extension, input_message)
    except ValueError as e:
        return True, str(e)


def print_dict(xml, l=0):
    if type(xml)==dict:
        for i in xml:
            print(' '*l+str(i)+': ')
            print_dict(xml[i],l+len(str(i)))
    else:
        if type(xml)==list:
            for i in xml:
                print(' '*l+str(i))
        else:
            print(' '*l+str(xml))


def custom_escape(data):
    dangerous_characters = ["'", '"', ";", "--", "#", "<", ">", "&", "%", "(", ")", "{", "}", "[", "]", "\\", "*", "+",
                            "?", "!", "$", "@", "^", "|"]

    for char in dangerous_characters:
        data = data.replace(char, '')

    return data


def fill_dict():
    result = {}
    while True:
        key = custom_escape(input("Введите ключ ('exit' для выхода): "))
        if key.lower() == 'exit':
            break

        value_type = custom_escape(input("Введите тип для значения ('key' или 'value'): ").lower())

        if value_type == 'key':
            print("Заполнение вложенного словаря:")
            value = fill_dict()
        elif value_type == 'value':
            value = ''
            tmp = []
            while value != 'exit':
                value = custom_escape(input("Введите значение ('exit' для выхода): "))
                if value != 'exit':
                    tmp.append(value)
            tmp = ', '.join(tmp)
            value = tmp

        else:
            print("Неправильный тип. Пожалуйста, выберите key/value.")
            continue

        result[key] = value

    return result


def print_xml_element(element, indent=0):
    print(" " * indent + f"<{element.tag} {element.attrib}> {element.text}")
    for child in element:
        print_xml_element(child, indent + 4)
    print(" " * indent + f"</{element.tag}>")


def main(task_num: str):
    if task_num == "1.":
        print(f"Информации о системе:\nСистема: {platform.system()}")
        partitions = psutil.disk_partitions()

        for partition in partitions:
            print(f"Диск: {partition.device}")
            print(f"  Точка монтирования: {partition.mountpoint}")
            print(f"  Файловая система: {partition.fstype}")

            try:
                usage = psutil.disk_usage(partition.mountpoint)
                print(f"  Размер: {usage.total / (1024 ** 3):.2f} GB")
                print(f"  Использовано: {usage.used / (1024 ** 3):.2f} GB")
                print(f"  Свободно: {usage.free / (1024 ** 3):.2f} GB")
                print(f"  Процент использования: {usage.percent}%")
            except PermissionError:
                print("  Нет доступа для получения информации о диске.")

            print()
    elif task_num == "2.1.":
        need_return, file_path = get_file_with_value_error(".txt")

        if need_return:
            print(f"\n\033[31m{file_path}\033[0m")
            return

        # file_path = get_file_path(".txt")

        with open(file_path, 'w') as file:
            file.write("some")

        print(f"Файл '{file_path}' успешно создан.")
    elif task_num == "2.2.":
        need_return, file_path = get_file_with_value_error(".txt")

        if need_return:
            print(f"\n\033[31m{file_path}\033[0m")
            return

        # file_path = get_file_path(".txt")
        # ../1.txt
        user_text = input("Введите строку для записи в файл: ")
        with open(file_path, 'w') as file:
            file.write(user_text)
        print(f"Строка '{user_text}' успешно записана в '{file_path}'")
    elif task_num == "2.3.":
        need_return, file_path = get_file_with_value_error(".txt")

        if need_return:
            print(f"\n\033[31m{file_path}\033[0m")
            return

        # file_path = get_file_path(".txt")

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read()

            print(f"Содержимое файла '{file_path}':\n{content}")
        else:
            print(f"Файл '{file_path}' не найден.")
    elif task_num == "2.4.":
        need_return, file_path = get_file_with_value_error(".txt")

        if need_return:
            print(f"\n\033[31m{file_path}\033[0m")
            return

        # file_path = get_file_path(".txt")

        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Файл '{file_path}' удалён.")
        else:
            print(f"Файл '{file_path}' не найден.")
    elif task_num == "3.2.":
        need_return, file_path = get_file_with_value_error(".json")

        if need_return:
            print(f"\n\033[31m{file_path}\033[0m")
            return

        # file_path = get_file_path(".json")

        try:
            json_data = fill_dict()

            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(json_data, file, ensure_ascii=False, indent=4)
            print(f"JSON '{json_data}' успешно записан в '{file_path}'")
        except json.JSONDecodeError:
            print("Ошибка: введены некорректные данные JSON.")
    elif task_num == "3.3.":
        need_return, file_path = get_file_with_value_error(".json")

        if need_return:
            print(f"\n\033[31m{file_path}\033[0m")
            return

        # file_path = get_file_path(".json")

        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                    print(f"Содержимое файла '{file_path}':")
                    print_dict(data)
                    # dump_data = json.dumps(data, ensure_ascii=False, indent=4)
                    #
                    # print(f"Содержимое файла '{file_path}':\n{dump_data}")
            except json.JSONDecodeError:
                print(f"Ошибка: '{file_path}' содержит некорректные данные.")
        else:
            print(f"Файл '{file_path}' не найден.")
    elif task_num == "3.4.":
        need_return, file_path = get_file_with_value_error(".json")

        if need_return:
            print(f"\n\033[31m{file_path}\033[0m")
            return

        # file_path = get_file_path(".json")

        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Файл '{file_path}' удалён.")
        else:
            print(f"Файл '{file_path}' не найден.")
    elif task_num == "4.2.":
        need_return, file_path = get_file_with_value_error(".xml")

        if need_return:
            print(f"\n\033[31m{file_path}\033[0m")
            return

        # file_path = get_file_path(".xml")

        # tag = check_symbols(input("Введите имя тега: "), allowed_letters)
        # text = check_symbols(input(f"Введите текст для тега {tag}: "), allowed_letters)
        #
        # root = ET.Element("data")
        #
        # item1 = ET.SubElement(root, "item")
        # item1.set("name", tag)
        # item1.text = text
        #
        # tree = ET.ElementTree(root)

        # tree = ET.parse(file_path)
        # root = tree.getroot()
        #
        # new_element = ET.Element(tag)
        # new_element.text = text
        # root.append(new_element)
        inp1 = custom_escape(input('Введите корневой элемент: '))
        data = fill_dict()

        root = ET.Element(inp1)

        def add_items(parent, data_dict):
            for key, value in data_dict.items():
                child = ET.SubElement(parent, key)
                if type(value) == dict:
                    add_items(child, value)
                else:
                    child.text = str(value)

        add_items(root, data)

        tree = ET.ElementTree(root)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)
        print(f"Введённые данные успешно записаны в '{file_path}'")
    elif task_num == "4.3.":
        need_return, file_path = get_file_with_value_error(".xml")

        if need_return:
            print(f"\n\033[31m{file_path}\033[0m")
            return

        # file_path = get_file_path(".xml")

        try:
            tree = ET.parse(file_path)
            # root = tree.getroot()

            print("Содержимое файла XML:")
            # print_xml_element(root)
            # print_dict(tree.__dict__)
            with open(file_path, "r", encoding='utf-8') as f:
                xml_read = f.read()

                parsed_string = parseString(xml_read)
                pretty_xml = parsed_string.toprettyxml()

                dict_xml = xmltodict.parse(pretty_xml)
                print_dict(dict_xml)
        except xml.etree.ElementTree.ParseError:
            print("Неверный xml файл")
    elif task_num == "4.4.":
        file_path = get_file_path(".xml")

        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Файл '{file_path}' удалён.")
        else:
            print(f"Файл '{file_path}' не найден.")
    elif task_num == "5.1.":
        need_return, file_path = get_file_with_value_error(".zip")

        if need_return:
            print(f"\n\033[31m{file_path}\033[0m")
            return

        # file_path = get_file_path(".zip")

        with zipfile.ZipFile(file_path, 'w'):
            pass

        print(f"Архив '{file_path}' создан.")
    elif task_num == "5.2.":
        need_return, file_path = get_file_with_value_error(".zip")

        if need_return:
            print(f"\n\033[31m{file_path}\033[0m")
            return

        # file_path = get_file_path(".zip")
        input_message = f"Введите имя файла c расширением .txt для архивации: "
        file_to_archive_path = get_file_path(".txt", input_message)

        try:
            with zipfile.ZipFile(file_path, 'w') as zipf:
                zipf.write(file_to_archive_path, os.path.basename(file_to_archive_path))
                print(f"Файл '{file_to_archive_path}' добавлен в архив '{file_path}'.")
        except FileNotFoundError:
            print(f"Файл '{file_to_archive_path}' не найден.")
    elif task_num == "5.3.":
        need_return, file_path = get_file_with_value_error(".zip")

        if need_return:
            print(f"\n\033[31m{file_path}\033[0m")
            return

        # file_path = get_file_path(".zip")
        extract_to = os.path.join(os.getcwd(), "extract")

        with zipfile.ZipFile(file_path, 'r') as zipf:
            zipf.extractall(extract_to)
            print(f"Файлы извлечены в директорию '{extract_to}'.")

        archive_size = os.path.getsize(file_path)
        print(f"Размер архива {file_path}: {archive_size} байт.")
    elif task_num == "5.4.":
        input_message = f"Введите имя файла c расширением .zip для удаления: "
        need_return, file_path = get_file_with_value_error(".zip", input_message)

        if need_return:
            print(f"\n\033[31m{file_path}\033[0m")
            return

        # file_path = get_file_path(".zip", input_message)
        input_message = f"Введите имя файла c расширением .txt для удаления: "
        need_return, source_file_path = get_file_with_value_error(".txt", input_message)

        if need_return:
            print(f"\n\033[31m{source_file_path}\033[0m")
            return

        # source_file_path = get_file_path(".txt", input_message)

        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Файл '{file_path}' удален.")
        else:
            print(f"Файл '{file_path}' не найден.")

        if os.path.exists(source_file_path):
            os.remove(source_file_path)
            print(f"Файл '{source_file_path}' удален.")
        else:
            print(f"Файл '{source_file_path}' не найден.")
    else:
        print(f"\033[31mНеизвестный номер '{task_num}'\033[0m")


if __name__ == "__main__":
    try:
        main(input(task_description))
    except KeyboardInterrupt:
        print("\n\033[31mОперация отменена.\033[0m")
