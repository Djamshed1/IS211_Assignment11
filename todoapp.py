#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Week 11 todoapp assignment"""

from flask import Flask, render_template, request, redirect
import re
import pickle
import os.path

app = Flask(__name__)

toDoList = []
email_mask = re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

def load():
    File_Name = 'toDoList.pkg1'
    if os.path.exists(File_Name):
        return pickle.load(open(File_Name, 'rb'))
    else:
        return []

@app.route('/')
def hello_world():
    return render_template('index.html', toDoList=toDoList)

@app.route('/submit', methods=['POST'])
def submit():

    task_name = request.form['task_name']
    email_address = request.form['email_address']
    priority_level = request.form['priority_level']

    if re.match(email_mask, email_address) is None:
        return redirect('/')
    elif len(task_name) == 0:
        return redirect('/')
    elif priority_level not in ('low', 'medium', 'high'):
        return redirect('/')
    else:
        toDoList.append((email_address, task_name, priority_level))
        return redirect('/')

@app.route('/clear', methods=['POST'])
def clear():
    toDoList[:] = []
    return redirect('/')

@app.route('/delete', methods=['POST'])
def delete():
    email_address = request.form['email_address']
    deletetask_name = request.form['deletetask_name']
    priority_level = request.form['priority_level']
    entry = (email_address, deletetask_name, priority_level)
    toDoList.remove(entry)
    return redirect('/')

@app.route('/save', methods=['POST'])
def save():
    pickle.dump(toDoList, open('toDoList.pkg1', 'wb'))
    return redirect('/')

if __name__ == "__main__":
    toDoList = load()
    app.run()
