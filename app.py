# app.py

import os
from flask import Flask, render_template, redirect, url_for, jsonify, send_from_directory
import poembot_final
from peewee import *
import datetime
# import nltk

app = Flask(__name__)
db = SqliteDatabase('poems.db')

@app.route('/')
def hello():
    return "Hello world!"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, ''), 'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    # if id in poems, delete it.
    poem = Poem.get(Poem.id == id)
    poem.delete_instance()
    return redirect(url_for('poems'))
    
@app.route('/poems')
def poems():
    poems = Poem.select().order_by(Poem.id.desc())

    # return jsonify(list(poems.dicts()))
    return render_template('poems.html', poems=poems)

@app.route('/poem')
def poem():
    title, poem = poembot_final.generate_poem()
    timestamp = datetime.datetime.now()

    new_poem = Poem(body=poem, title=title, created_at=timestamp)
    new_poem.save()
    
    return redirect(url_for('poems'))
    # return render_template('poem.html', title=title, poem=poem)

class Poem(Model):
    body = CharField()
    title = CharField()
    created_at = DateField()

    class Meta:
        database = db

# @app.route('/python')
# def python():

if __name__ == '__main__':
    app.run(debug=True)
