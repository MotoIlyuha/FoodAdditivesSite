from flask import render_template, request, redirect, jsonify
from create_db import *


def get_additives(synonym, category=None, limit=50):
    matching_synonyms = Synonym.query.filter(Synonym.name.like(f'%{synonym}%')).all()

    # Собрать идентификаторы связанных синонимами объектов Data
    data_ids = [synonym.data_id for synonym in matching_synonyms]

    # Получить данные Data и связанные с ними объекты Danger, Category и Origin
    if category is None:
        data_query = Data.query \
            .join(Danger) \
            .join(Category, Data.categories) \
            .join(Origin, Data.origins) \
            .filter(Data.id.in_(data_ids)) \
            .order_by(Data.code) \
            .limit(limit)
    else:
        data_query = Data.query \
            .join(Danger) \
            .join(Category, Data.categories) \
            .join(Origin, Data.origins) \
            .filter(Category.name == category) \
            .filter(Data.id.in_(data_ids)) \
            .order_by(Data.code) \
            .limit(limit)

    # Извлечь необходимые поля из результата запроса
    result = data_query.with_entities(Data.code, Data.name, Danger.name, Category.name, Origin.name).all()

    # Преобразовать результат в список словарей для удобства использования
    data = []
    for row in result:
        data.append({
            'code': row[0],
            'name': row[1],
            'danger': row[2],
            'categories': row[3:],
            'origins': row[3:]
        })
    return data


@app.route('/')
def index():
    data = get_additives("", limit=10)
    return render_template('index.html', additives=data)


@app.route('/additives')
def additives():
    data = get_additives('')
    return render_template('additives.html', item=data, categories=additives_categories)


@app.route('/additives/<category>')
def additives_category(category):
    data = get_additives("", category)
    return render_template('additives.html', item=data, categories=additives_categories, category=category)


@app.route('/additives/<category>/process')
def additives_category_process(category):
    text = request.form['text']
    data = get_additives(text, category)
    return jsonify(data)


@app.route('/additives/process', methods=['POST'])
def process():
    text = request.form['text']
    data = get_additives(text)
    print(data)
    return jsonify(data)


@app.route('/info')
def info():
    return render_template('info.html')


if __name__ == '__main__':
    app.run(debug=True)
