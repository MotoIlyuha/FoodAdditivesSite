from flask import render_template, request, redirect, jsonify
from create_db import *


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/additives')
def additives():
    additives_categories = [category[0] for category in db.session.query(Category.name).all()]
    return render_template('additives.html', categories=additives_categories)


@app.route('/additives/<category>')
def additives_category(category):
    print(category)
    additives_categories = [category[0] for category in db.session.query(Category.name).all()]
    return render_template('additives.html', categories=additives_categories)


@app.route('/additives/process', methods=['POST'])
def process():
    text = request.form['text']
    add_ids = set([id_[0] for id_ in db.session.query(Synonym.data_id).filter(Synonym.name.like(f"%{text}%")).all()])
    adds = []
    for add_id in add_ids:
        add = db.session.query(Data).filter(Data.id == add_id).first()
        adds.append({'code': add.code, 'name': add.name, 'danger': add.danger_id, 'categories': add.categories,
                     'origins': add.origins})
    print(text, adds)
    return jsonify(adds)


@app.route('/info')
def info():
    return render_template('info.html')


if __name__ == '__main__':
    app.run(debug=True)
