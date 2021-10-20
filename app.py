from flask import Flask, request, render_template, url_for, redirect, make_response, flash
from random import randint

app = Flask(__name__)

def genCode(cookies):
    code = randint(1, 1000000)
    if code in cookies:
        genCode()
    return code

@app.route('/', methods=['GET', 'POST'])
def index():
    res = make_response(render_template('index.html', tasks=request.cookies, bool=bool))

    if request.method == 'POST':
        task = request.form.get('task')
        return redirect(url_for('add_task', task=task))
    
    return res

@app.route('/add_task/<task>')
def add_task(task):
    code = genCode(request.cookies)
    res = make_response(redirect(url_for('index')))
    res.set_cookie(f'todo{code}', f'{task}--=||=--False')

    return res

@app.route('/complete_task/<task>/<title>')
def complete_task(task, title):
    res = make_response(redirect(url_for('index')))
    res.set_cookie(title, f'{task}--=||=--True')

    return res

@app.route('/uncomplete_task/<task>/<title>')
def uncomplete_task(task, title):
    res = make_response(redirect(url_for('index')))
    res.set_cookie(title, f'{task}--=||=--False')

    return res

@app.route('/remove_task/<task>/<title>')
def remove_task(task, title):
    res = make_response(redirect(url_for('index')))
    res.delete_cookie(title)

    return res

@app.route('/remove_all_tasks')
def remove_all_tasks():
    res = make_response(redirect(url_for('index')))
    for keys, item in request.cookies.items():
        res.delete_cookie(keys)
    return res

@app.route('/remove_all_completed')
def remove_all_completed():
    res = make_response(redirect(url_for('index')))
    for key, item in request.cookies.items():
        if item.split('--=||=--')[1] == 'True':
            res.delete_cookie(key)
    return res

if __name__ == '__main__':
    app.run(port=5000)