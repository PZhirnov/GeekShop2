import json
import os.path

with open(r'mainapp/json/contacts.json', "r", encoding='utf8') as jsonfile:
    data = json.load(jsonfile)


# проверяем вывод
print(type(data))
print(data)

# вывод пути к текущим файлам
print(os.path.dirname(__file__))  # путь к папке, в которой лежим файл
print(__file__)  # полный путь к текущему файлу


test_dict = {
    "один": 1,
    "два": 2,
    "три": 3,
}

print(test_dict)
print(len(test_dict.keys()))

for key, val in test_dict.items():
    print(key, val)
