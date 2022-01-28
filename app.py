#!/usr/bin/python3
'''
this script creates a page to return hello hbnb
'''
from urllib import request
from flask import Flask, render_template, request, redirect
import sqlite3
import json
app = Flask(__name__)
con = sqlite3.connect('example.db', check_same_thread=False)
cur = con.cursor()

@app.route('/', strict_slashes=False)
def redirectToLogin():
    return redirect('/loginPage')

@app.route('/loginPage', strict_slashes=False)
def loginPage():
    '''This method creates a route and gives it some text'''
    return render_template('loginPage.html')

@app.route('/loginPage', strict_slashes=False, methods=['POST'])
def loginPagePost():
    '''This method creates a route and gives it some text'''
    if cur.execute('SELECT * FROM users WHERE username = "{}"'.format(request.form['username'])).fetchall() == []:
        return "Invalid Username!"

    else:
        if cur.execute('SELECT * FROM users WHERE username = "{}" AND password = "{}"'.format(request.form['username'], request.form['password'])).fetchall() == []:
            return "Invalid Password!"
        else:
            return redirect('/overview/{}'.format(request.form['username']))

@app.route('/overview/<username>', strict_slashes=False)
def homePage(username):
    '''This method creates a route and gives it some text'''
    userData = cur.execute('SELECT * FROM users WHERE username = "{}"'.format(username)).fetchall()[0]
    expenses = json.loads(cur.execute('SELECT * FROM users WHERE username = "{}"'.format(username)).fetchall()[0][4])
    incomes = json.loads(cur.execute('SELECT * FROM users WHERE username = "{}"'.format(username)).fetchall()[0][5])
    incomeSum = 0
    for i in incomes:
        incomeSum+= i[1]
    expenseSum = 0
    for i in expenses:
        expenseSum+= i[1]
    round(incomeSum, 2)
    round(expenseSum, 2)
    totalSum = round((incomeSum - expenseSum), 2)
    return render_template('overview.html', userData=userData, username=username, expenses=expenses, incomes=incomes, incomeSum=incomeSum, expenseSum=expenseSum, totalSum=totalSum)

@app.route('/overview/<username>/addExpense', strict_slashes=False)
def addExpense(username):
    return render_template('addExpense.html')

@app.route('/overview/<username>/addExpense', methods=['POST'], strict_slashes=False)
def addExpensePost(username):
    #cur.execute("UPDATE users SET incomes = incomes || '{}' WHERE user_id = '{}'".format([], username))
    #request.form[''] #expName expAmt expCat
    return redirect('/overview/{}'.format(username))

@app.route('/friends', strict_slashes=False)
def friendsPage():
    '''This method creates a route and gives it some text'''
    return render_template('friends.html')

@app.route('/lists', strict_slashes=False)
def listsPage():
    '''This method creates a route and gives it some text'''
    return render_template('lists.html')

@app.route('/settings', strict_slashes=False)
def settingsPage():
    '''This method creates a route and gives it some text'''
    return render_template('settings.html')

@app.route('/user/<username>', strict_slashes=False)
def displayUserInfo(username=None):
    '''displays info from SQLite about user'''
    if username is not None:
        userInfo = cur.execute('SELECT * FROM users WHERE username = "{}"'.format(username)).fetchall()
        return render_template("userInfo.html", userInfo=userInfo)
    else:
        return render_template('Username / Password not found')

@app.route('/users/', strict_slashes=False)
def displayUsers():
    '''displays info from SQLite about user'''
    users = cur.execute('SELECT * FROM users').fetchall()
    return render_template("users.html", users=users)


if __name__ == '__main__':
    '''this method sets everything to work on 0.0.0.0'''
    #app.debug = True
    app.run(host='0.0.0.0', port=5000)
