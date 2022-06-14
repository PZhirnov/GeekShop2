import json

data = {
    "user_login": {
        "name": "Ivan Ivanov",
        "city": "Moscow",
        "status": "Gold",
        "balance": 5800,
        "bonus": 2000
    }
}

# сохраняем в файл
with open("users_bd.json", "w") as write_file:
    json.dump(data, write_file)


with open("users_bd.json", "r") as read_file:
    data = json.load(read_file)

print(type(data))
print(data)

# получим нужные данные
print(data.get('user_login'))

res = {}
res = data.get('user_login')
print(type(res))
for i, j in res.items():
    print(i, j)


def user_info(name):
    with open("users_bd.json", "r") as read_file:
        data_user = json.load(read_file)
    return data_user.get(name)


user = user_info('user_login')

print(user)

