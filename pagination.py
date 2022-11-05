
from flask import Flask, request, jsonify

items = [

    {"pk": 1, "letter": "a"},
    {"pk": 2, "letter": "b"},
    {"pk": 3, "letter": "c"},
    {"pk": 4, "letter": "d"},
    {"pk": 5, "letter": "e"},

    {"pk": 6, "letter": "f"},
    {"pk": 7, "letter": "g"},
    {"pk": 8, "letter": "h"},
    {"pk": 9, "letter": "i"},
    {"pk": 10, "letter": "j"},

    {"pk": 11, "letter": "k"},
    {"pk": 12, "letter": "l"},
    {"pk": 13, "letter": "m"},
    {"pk": 14, "letter": "n"},
    {"pk": 15, "letter": "o"},

]

app = Flask(__name__)


@app.route('/items/')
def show_items_paginated():

    # Получаем номер страницы (по умолчанию = 1)
    page = int(request.args.get('page', 1))

    # Устанавливаем количество на страницу (лучше вынести в константу или настройки приложения)
    items_per_page = 5

    # Вычисляем начало и конец выборки
    pagination_from = (page - 1) * items_per_page
    pagination_to = page * items_per_page

    # Получаем срез
    items_paginated = items[pagination_from:pagination_to]

    # Возвращаем значения

    return jsonify(items_paginated)


if __name__ == '__main__':
    app.run(debug=True)