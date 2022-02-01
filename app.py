#!/usr/bin/python3
'''
this script creates a page to return hello hbnb
'''
from urllib import request
import uuid
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import json
from uuid import uuid4

from matplotlib.font_manager import json_dump
app = Flask(__name__)
con = sqlite3.connect('example.db', check_same_thread=False)
con.row_factory = sqlite3.Row
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
        return redirect('/loginPage/createUser/{}/{}'.format(request.form['username'], request.form['password']))

    else:
        if cur.execute('SELECT * FROM users WHERE username = "{}" AND password = "{}"'.format(request.form['username'], request.form['password'])).fetchall() == []:
            return "Invalid Password!"
        else:
            return redirect('/overview/{}'.format(request.form['username']))

@app.route('/overview/<username>', strict_slashes=False)
def homePage(username):
    '''This method creates a route and gives it some text'''
    expenses = json.loads(cur.execute('SELECT * FROM users WHERE username = "{}"'.format(username)).fetchall()[0]['expenses'])
    incomes = json.loads(cur.execute('SELECT * FROM users WHERE username = "{}"'.format(username)).fetchall()[0]['incomes'])
    incomeSum = 0
    for i in incomes:
        incomeSum+= i[1]
    expenseSum = 0
    for i in expenses:
        expenseSum+= i[1]
    round(incomeSum, 2)
    round(expenseSum, 2)
    totalSum = round((incomeSum - expenseSum), 2)
    return render_template('overview.html', username=username, expenses=expenses, incomes=incomes, incomeSum=incomeSum, expenseSum=expenseSum, totalSum=totalSum)

@app.route('/overview/<username>/addExpense', strict_slashes=False)
def addExpense(username):
    return render_template('addExpense.html')

@app.route('/overview/<username>/addExpense', methods=['POST'], strict_slashes=False)
def addExpensePost(username):
    expenses = json.loads(cur.execute('SELECT expenses FROM users WHERE username = "{}"'.format(username)).fetchall()[0][0])
    expenses.append([request.form['expName'], round(float(request.form['expAmt'].replace(',', '')), 2), request.form['expCat']])
    cur.execute("UPDATE users SET expenses = '{}' WHERE username = '{}'".format(json.dumps(expenses), username))
    con.commit()
    return redirect('/overview/{}'.format(username))

@app.route('/overview/<username>/addIncome', strict_slashes=False)
def addIncome(username):
    return render_template('addIncome.html')

@app.route('/overview/<username>/addIncome', methods=['POST'], strict_slashes=False)
def addIncomePost(username):
    incomes = json.loads(cur.execute('SELECT incomes FROM users WHERE username = "{}"'.format(username)).fetchall()[0][0])
    incomes.append([request.form['incName'], round(float(request.form['incAmt'].replace(',', '')), 2), request.form['incCat']])
    cur.execute("UPDATE users SET incomes = '{}' WHERE username = '{}'".format(json.dumps(incomes), username))
    con.commit()
    return redirect('/overview/{}'.format(username))

@app.route('/<username>/friends', strict_slashes=False)
def friendsPage(username):
    '''This method creates a route and gives it some text'''
    friendsInfo=json.loads(cur.execute('SELECT friends FROM users WHERE username = "{}"'.format(username)).fetchall()[0][0])
    return render_template('friends.html', friendsInfo=friendsInfo, username=username)

@app.route('/<username>/friends', methods=['POST'], strict_slashes=False)
def friendsPagePost(username):
    '''This method creates a route and gives it some text'''
    if cur.execute('SELECT username FROM users WHERE username = "{}"'.format(request.form['friendUserName'])).fetchall() == []:
        return "This user does not exist"
    else:
        friendsList = json.loads(cur.execute('SELECT friends FROM users WHERE username = "{}"'.format(username)).fetchall()[0][0])
        friendUserName = request.form['friendUserName']
        friendId = cur.execute('SELECT user_id FROM users WHERE username = "{}"'.format(friendUserName)).fetchall()[0][0]
        friendsList.append({"username": friendUserName, "user_id": friendId})
        cur.execute("UPDATE users SET friends = '{}' WHERE username = '{}'".format(json.dumps(friendsList), username))
        con.commit()
        return redirect('/<username>/friends')


@app.route('/lists', strict_slashes=False)
def listsPage():
    '''This method creates a route and gives it some text'''
    return render_template('lists.html')

@app.route('/settings', strict_slashes=False)
def settingsPage():
    '''This method creates a route and gives it some text'''
    return render_template('settings.html')

@app.route('/api/users/<username>', strict_slashes=False)
def displayUserInfo(username=None):
    '''displays info from SQLite about user'''
    response = cur.execute('SELECT * FROM users where username = "{}"'.format(username)).fetchall()
    if username is not None:
        for r in response:
            dic = {r.keys()[i]: r[i] for i in range(len(r))}
        return (json.dumps(dic))
    else:
        return('user not found')

@app.route('/api/users/', strict_slashes=False)
def displayUsers():
    '''displays info from SQLite about users'''
    usersList = []
    response = cur.execute('SELECT * FROM users').fetchall()
    for r in response:
        dic = {r.keys()[i]: r[i] for i in range(len(r))}
        usersList.append(dic)
    return(json.dumps(usersList))

@app.route('/loginPage/createUser/<username>/<password>', strict_slashes=False)
def createUser(username, password):
    '''displays info from SQLite about user'''
    return render_template("createUser.html", username=username, password=password)

@app.route('/loginPage/createUser/<username>/<password>', methods=['POST'], strict_slashes=False)
def createUserPost(username, password):
    '''displays info from SQLite about user'''
    cur.execute("INSERT INTO users VALUES ('{}','{}', '{}', '', '{}', '{}', '{}', '')".format(username, password, str(uuid.uuid4()), json.dumps([]), json.dumps([]), json.dumps([])))
    con.commit()
    return redirect('/overview/{}'.format(username))

@app.route('/api/users')
def apiDisplayUsers():
    userList = []
    response = cur.execute('SELECT * FROM users').fetchall()
    for r in response:
        userDic = {r.keys()[i]: r[i] for i in range(len(r))}
        userList.append(userDic)
    return(json.dumps(userList))


@app.route('/api/users/<username>')
def apiDisplayUser(username):
    response = cur.execute('SELECT * FROM users WHERE username = "{}"'.format(username)).fetchall()
    for r in response:
        userDic = {r.keys()[i]: r[i] for i in range(len(r))}
    return(json.dumps(userDic))

if __name__ == '__main__':
    '''this method sets everything to work on 0.0.0.0'''
    #app.debug = True
    app.run(host='0.0.0.0', port=5000)
