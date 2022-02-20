#!/usr/bin/python3
'''
this script creates a page to return hello hbnb
'''
from cmath import exp
from urllib import request, response
import uuid
from flask import Flask, render_template, redirect, url_for, make_response
from flask import request as rq
import sqlite3
import json
from uuid import uuid4
from secrets import token_hex

app = Flask(__name__)
app.static_url_path=''
app.static_folder='static'
app.template_folder='templates'
app.secret_key = token_hex()
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
    response = make_response(redirect(url_for('homePage')))
    response.set_cookie('username', rq.form['username'])
    response.set_cookie('password', rq.form['password'])
    response.set_cookie('user_id', cur.execute('SELECT user_id FROM users WHERE username = "{}"'.format(rq.form['username'])).fetchall()[0][0])
    if cur.execute('SELECT * FROM users WHERE username = "{}"'.format(rq.form['username'])).fetchall() == []:
        return redirect('/loginPage/createUser/'.format(rq.form['username'], rq.form['password']))
    else:
        if cur.execute('SELECT * FROM users WHERE username = "{}" AND password = "{}"'.format(rq.form['username'], rq.form['password'])).fetchall() == []:
            return "Invalid Password!"
        else:
            return response

@app.route('/overview', strict_slashes=False)
def homePage():
    '''This method creates a route and gives it some text'''
    username = rq.cookies.get('username')
    expenses = json.loads(cur.execute('SELECT expenses FROM lists WHERE owner_id = "{}"'.format(rq.cookies['user_id'])).fetchall()[0][0])
    incomes = json.loads(cur.execute('SELECT incomes FROM lists WHERE owner_id = "{}"'.format(rq.cookies['user_id'])).fetchall()[0][0])
    incomeSum = 0
    for i in incomes:
        incomeSum+= i[1]
    expenseSum = 0
    for i in expenses:
        expenseSum+= i[1]
    incomeSum = round(incomeSum, 2)
    expenseSum = round(expenseSum, 2)
    totalSum = round((incomeSum - expenseSum), 2)
    return render_template('overview.html', username=username, expenses=expenses, incomes=incomes, incomeSum=incomeSum, expenseSum=expenseSum, totalSum=totalSum)

@app.route('/overview/addExpense', strict_slashes=False)
def addExpense():
    return render_template('addExpense.html')

@app.route('/overview/addExpense', methods=['POST'], strict_slashes=False)
def addExpensePost():
    username =  rq.cookies.get('username')
    expenses = json.loads(cur.execute('SELECT expenses FROM users WHERE username = "{}"'.format(username)).fetchall()[0][0])
    expenses.append([rq.form['expName'], round(float(rq.form['expAmt'].replace(',', '')), 2), rq.form['expCat']])
    cur.execute("UPDATE users SET expenses = '{}' WHERE username = '{}'".format(json.dumps(expenses), username))
    con.commit()
    return redirect('/overview')

@app.route('/overview/addIncome', strict_slashes=False)
def addIncome():
    return render_template('addIncome.html')

@app.route('/overview/addIncome', methods=['POST'], strict_slashes=False)
def addIncomePost():
    username = rq.cookies.get('username')
    incomes = json.loads(cur.execute('SELECT incomes FROM users WHERE username = "{}"'.format(username)).fetchall()[0][0])
    incomes.append([rq.form['incName'], round(float(rq.form['incAmt'].replace(',', '')), 2), rq.form['incCat']])
    cur.execute("UPDATE users SET incomes = '{}' WHERE username = '{}'".format(json.dumps(incomes), username))
    con.commit()
    return redirect('/overview'.format(username))

@app.route('/friends', strict_slashes=False)
def friendsPage():
    '''This method creates a route and gives it some text'''
    username = rq.cookies.get('username')
    friendsInfo=json.loads(cur.execute('SELECT friends FROM users WHERE username = "{}"'.format(username)).fetchall()[0][0])
    return render_template('friends.html', friendsInfo=friendsInfo, username=username)

@app.route('/friends', methods=['POST'], strict_slashes=False)
def friendsPagePost():
    '''This method creates a route and gives it some text'''
    username = rq.cookies.get('username')
    if cur.execute('SELECT username FROM users WHERE username = "{}"'.format(rq.form['friendUserName'])).fetchall() == []:
        return "This user does not exist"
    else:
        friendsList = json.loads(cur.execute('SELECT friends FROM users WHERE username = "{}"'.format(username)).fetchall()[0][0])
        friendUserName = rq.form['friendUserName']
        friendId = cur.execute('SELECT user_id FROM users WHERE username = "{}"'.format(friendUserName)).fetchall()[0][0]
        friendsList.append({"username": friendUserName, "user_id": friendId})
        cur.execute("UPDATE users SET friends = '{}' WHERE username = '{}'".format(json.dumps(friendsList), username))
        con.commit()
        return redirect('/friends')


@app.route('/lists', strict_slashes=False)
def listsPage():
    '''This method creates a route and gives it some text'''
    username = rq.cookies.get('username')
    lists = cur.execute("SELECT * from lists WHERE owner_name = '{}'".format(username))
    return render_template('lists.html', username=username, lists=lists)

@app.route('/lists', strict_slashes=False, methods=['POST'])
def listsPagePost():
    '''This method creates a route and gives it some text'''
    username = rq.cookies.get('username')
    user_id = cur.execute("SELECT user_id FROM users where username = '{}'".format(username)).fetchall()[0][0]
    cur.execute("INSERT INTO lists VALUES ('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
    rq.form['listName'],
    str(uuid.uuid4()),
    user_id,
    username,
    json.dumps([]),
    json.dumps([]),
    json.dumps([]),
    json.dumps([]),
    json.dumps([])
    )
    )
    con.commit()
    return redirect('/lists'.format(username))

@app.route('/lists/<listName>', strict_slashes=False)
def listData(listName):
    username = rq.cookies.get('username')
    expenses = json.loads(cur.execute('SELECT expenses FROM lists WHERE owner_name = "{}" AND list_name = "{}"'.format(username, listName)).fetchall()[0][0])
    incomes = json.loads(cur.execute('SELECT incomes FROM lists WHERE owner_name = "{}" AND list_name = "{}"'.format(username, listName)).fetchall()[0][0])
    incomeSum = 0
    for i in incomes:
        incomeSum+= i[1]
    expenseSum = 0
    for i in expenses:
        expenseSum+= i[1]
    incomeSum = round(incomeSum, 2)
    expenseSum = round(expenseSum, 2)
    totalSum = round((incomeSum - expenseSum), 2)
    return render_template('listData.html', username=username, listName=listName, expenses=expenses, incomes=incomes, incomeSum=incomeSum, expenseSum=expenseSum, totalSum=totalSum)

@app.route('/lists/<listName>/addExpense', strict_slashes=False)
def addListExpense(listName):
    return render_template('addListExpense.html')

@app.route('/lists/<listName>/addExpense', methods=['POST'], strict_slashes=False)
def addListExpensePost(listName):
    username = rq.cookies.get('username')
    expenses = json.loads(cur.execute('SELECT expenses FROM lists WHERE list_name = "{}"'.format(listName)).fetchall()[0][0])
    expenses.append([rq.form['expName'], round(float(rq.form['expAmt'].replace(',', '')), 2), rq.form['expCat']])
    cur.execute("UPDATE lists SET expenses = '{}' WHERE list_name = '{}'".format(json.dumps(expenses), listName))
    con.commit()
    return redirect('/lists/{}'.format(listName))

@app.route('/list/<listName>/addIncome', strict_slashes=False)
def addListIncome(listName):
    return render_template('addListIncome.html')

@app.route('/list/<listName>/addIncome', methods=['POST'], strict_slashes=False)
def addListIncomePost(listName):
    username = rq.cookies.get('username')
    incomes = json.loads(cur.execute('SELECT incomes FROM lists WHERE list_name = "{}"'.format(listName)).fetchall()[0][0])
    incomes.append([rq.form['incName'], round(float(rq.form['incAmt'].replace(',', '')), 2), rq.form['incCat']])
    cur.execute("UPDATE lists SET incomes = '{}' WHERE list_name = '{}'".format(json.dumps(incomes), listName))
    con.commit()
    return redirect('/lists/{}'.format(listName))

@app.route('/settings', strict_slashes=False)
def settingsPage():
    '''This method creates a route and gives it some text'''
    return render_template('settings.html')

@app.route('/loginPage/createUser', strict_slashes=False)
def createUser():
    '''displays info from SQLite about user'''
    username = rq.cookies.get('username')
    password = rq.cookies.get('password')
    return render_template("createUser.html", username=username, password=password)

@app.route('/loginPage/createUser', methods=['POST'], strict_slashes=False)
def createUserPost():
    '''displays info from SQLite about user'''
    username = rq.cookies.get('username')
    password = rq.cookies.get('password')
    cur.execute("INSERT INTO users VALUES ('{}','{}', '{}', '', '{}', '{}', '{}', '')".format(username, password, str(uuid.uuid4()), json.dumps([]), json.dumps([]), json.dumps([])))
    con.commit()
    return redirect('/overview')








#API

@app.route('/api', strict_slashes=False)
def displayAPIinfo():
    return("""/api/cookies<br>
              /api/users<br>
              /api/users/(user_id)<br>
              /api/users/(user_id)/username<br>
              /api/users/(user_id)/password<br>
              /api/users/(user_id)/lists/<br>
              /api/users/(user_id)/lists/(list_id)<br>
              /api/users/(user_id)/lists/(list_id)/name<br>
              /api/users/(user_id)/lists/(list_id)/categories<br>
              /api/users/(user_id)/lists/(list_id)/expenses<br>
              /api/users/(user_id)/lists/(list_id)/expenses/(id)<br>
              /api/users/(user_id)/lists/(list_id)/incomes<br>
              /api/users/(user_id)/lists/(list_id)/incomes/(id)<br>
              /api/users/(user_id)/lists/(list_id)/shared_users<br>
              /api/users/(user_id)/lists/(list_id)/list_settings<br>
              /api/users/(user_id)/friends<br>
              /api/users/(user_id)/settings<br>
            """
        )

@app.route('/api/cookies', strict_slashes=False)
def displayCookies(user_id=None):
    '''displays info from SQLite about user'''
    return json.dumps(rq.cookies)

@app.route('/api/users', strict_slashes=False)
def displayUsers():
    '''displays info from SQLite about users'''
    usersList = []
    response = cur.execute('SELECT * FROM users').fetchall()
    for r in response:
        dic = {r.keys()[i]: r[i] for i in range(len(r))}
        usersList.append(dic)
    return(json.dumps(usersList))

@app.route('/api/users', strict_slashes=False, methods=['POST'])
def postUser():
    '''This method creates a route and gives it some text'''
    request_content_type = rq.headers.get('Content-Type')
    jsonObj = rq.json
    responseStr = ""
    username = jsonObj.get('username')
    if username is None:
        return "requires username"
    elif username.replace(" ", "") == "":
        return "username cannot be blank."
    password = jsonObj.get('password')
    if password is None:
        return "requires password"
    elif password.replace(" ", "") == "":
        return "password cannot be blank."
    if (cur.execute("SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(username, password)).fetchall()) != []:
        return "user already exists!"
    friends = jsonObj.get('friends')
    if friends is None:
        responseStr = responseStr + " OPTIONAL: friends "
        friends = []
    else:
        try:
            friendsObj = json.loads(friends)
            new_friend_list = []
            for friend in friendsObj:
                if cur.execute("SELECT * FROM users where user_id = '{}'".format(friend)).fetchall() == []:
                    return "friend {} does not exist. (must use user_ids)".format(friend)
                else:
                    new_friend_list.append(friend)
            friends = new_friend_list
        except Exception:
            return "friends must be a valid json string."
    settings = jsonObj.get('settings')
    if settings is None:
        responseStr = responseStr + " OPTIONAL: settings "
        settings = []
    cur.execute("INSERT INTO users VALUES ('{}','{}', '{}', '{}', '{}', '{}')".format(username, password, str(uuid.uuid4()), json.dumps(lists), json.dumps(friends), json.dumps(settings)))
    con.commit()
    return "user created. " + responseStr


@app.route('/api/users/<user_id>', strict_slashes=False)
def displayUserInfo(user_id=None):
    '''displays info from SQLite about user'''
    response = cur.execute('SELECT * FROM users where user_id = "{}"'.format(user_id)).fetchall()
    if response != []:
        for r in response:
            dic = {r.keys()[i]: r[i] for i in range(len(r))}
        return (json.dumps(dic))
    else:
        return('user not found')

@app.route('/api/users/<user_id>', strict_slashes=False, methods=['POST'])
def PostUserInfo(user_id=None):
    '''This method creates a route and gives it some text'''
    if cur.execute("SELECT * FROM users where user_id = '{}'".format(user_id)).fetchall() == []:
        return "not a valid user_id"
    request_content_type = rq.headers.get('Content-Type')
    jsonObj = rq.json
    responseStr = ""
    new_username = jsonObj.get('new_username')
    if new_username is None:
        responseStr = responseStr + " OPTIONAL: new_username "
    elif new_username.replace(" ", "") == "":
        responseStr = responseStr + " new_username cannot be blank. value not updated "
    else:
        cur.execute("UPDATE users SET username = '{}' WHERE user_id = '{}'".format(new_username, user_id))
    new_password = jsonObj.get('new_password')
    if new_password is None:
        responseStr = responseStr + " OPTIONAL: new_password "
    elif new_password.replace(" ", "") == "":
        responseStr = responseStr + " new_password cannot be blank. value not updated "
    else:
        cur.execute("UPDATE users SET password = '{}' WHERE user_id = '{}'".format(new_password, user_id))
    friends = jsonObj.get('friends')
    if friends is None:
        responseStr = responseStr + " OPTIONAL: friends "
    else:
        try:
            friendsObj = json.loads(friends)
            new_friend_list = []
            for friend in friendsObj:
                if cur.execute("SELECT * FROM users where user_id = '{}'".format(friend)).fetchall() == []:
                    responseStr = responseStr + " friend {} does not exist. not updated. ".format(friend)
                else:
                    new_friend_list.append(friend)
            cur.execute("UPDATE users SET friends = '{}' where user_id = '{}'".format(json.dumps(list(set(new_friend_list))), user_id))
        except Exception:
            responseStr = responseStr + " friends must be a valid json string. not updated. "
    settings = jsonObj.get('settings')
    if settings is None:
        responseStr = responseStr + " OPTIONAL: settings "
    else:
        cur.execute("UPDATE users SET settings = '{}' where user_id = '{}'".format(settings, user_id))
    con.commit()
    return "user updated. " + responseStr

####################################
@app.route('/api/users/<user_id>', strict_slashes=False, methods=['PUT'])
def PutUserInfo(user_id=None):
    return "not yet implemented"

@app.route('/api/users/<user_id>/username', strict_slashes=False)
def displayUsername(user_id=None):
    '''displays info from SQLite about user'''
    response = cur.execute('SELECT username FROM users where user_id = "{}"'.format(user_id)).fetchall()
    if response != []:
        for r in response:
            dic = {r.keys()[i]: r[i] for i in range(len(r))}
        return (json.dumps(dic))
    else:
        return('user not found')

@app.route('/api/users/<user_id>/username', strict_slashes=False, methods=['POST'])
def postUsername(user_id=None):
    '''This method creates a route and gives it some text'''
    request_content_type = rq.headers.get('Content-Type')
    jsonObj = rq.json
    new_username = jsonObj.get('new_username')
    if cur.execute("SELECT * FROM users where user_id = '{}'".format(user_id)).fetchall() == []:
        return "not a valid user_id"
    if new_username is None:
        return "requires new_username"
    elif new_username.replace(" ", "") == "":
        return "new_username cannot be blank"
    else:
        cur.execute("UPDATE users SET username = '{}' WHERE user_id = '{}'".format(new_username, user_id))
        con.commit()
        return json.dumps('set user {} username to {}'.format(user_id, new_username))

@app.route('/api/users/<user_id>/password', strict_slashes=False)
def displayUserPassword(user_id=None):
    '''displays info from SQLite about user'''
    response = cur.execute('SELECT password FROM users where user_id = "{}"'.format(user_id)).fetchall()
    if response != []:
        for r in response:
            dic = {r.keys()[i]: r[i] for i in range(len(r))}
        return (json.dumps(dic))
    else:
        return('user not found')

@app.route('/api/users/<user_id>/password', strict_slashes=False, methods=['POST'])
def postPassword(user_id=None):
    '''This method creates a route and gives it some text'''
    request_content_type = rq.headers.get('Content-Type')
    jsonObj = rq.json
    if cur.execute("SELECT * FROM users where user_id = '{}'".format(user_id)).fetchall() == []:
        return "not a valid user_id"
    new_password = jsonObj.get('new_password')
    if new_password is None:
        return "requires new_password"
    elif new_password.replace(" ", "") == "":
        return "password cannot be blank"
    else:
        cur.execute("UPDATE users SET password = '{}' WHERE user_id = '{}'".format(new_password, user_id))
        con.commit()
        return json.dumps('set user {} username to {}'.format(user_id, new_password))

@app.route('/api/users/<user_id>/lists', strict_slashes=False)
def displayUserLists(user_id=None):
    '''displays info from SQLite about user'''
    response = cur.execute('SELECT lists FROM users where user_id = "{}"'.format(user_id)).fetchall()
    if response != []:
        dicList = []
        for r in response:
            dic = {r.keys()[i]: r[i] for i in range(len(r))}
            dicList.append(dic)
        return (json.dumps(dicList))
    else:
        return('user not found')

@app.route('/api/users/<user_id>/lists', strict_slashes=False, methods=['POST'])
def postList(user_id=None):
    '''This method creates a route and gives it some text'''
    request_content_type = rq.headers.get('Content-Type')
    if cur.execute("SELECT * FROM users where user_id = '{}'".format(user_id)).fetchall() == []:
        return "not a valid user_id"
    jsonObj = rq.json
    returnStr = ""
    list_name = jsonObj.get('list_name')
    if list_name is None:
        return "requires list_name."
    elif list_name.replace(" ", "") == "":
        return "list_name cannot be blank"
    list_id = str(uuid.uuid4())
    username = cur.execute("SELECT username FROM users where user_id = '{}'".format(user_id)).fetchall()[0][0]
    if username == []:
        return "user does not exist"
    categories = jsonObj.get('categories')
    if categories is None:
        categories = []
        returnStr = returnStr + " OPTIONAL: categories "
    expenses = jsonObj.get('expenses')
    if expenses is None:
        expenses = []
        returnStr = returnStr + " OPTIONAL: expenses "
    incomes = jsonObj.get('incomes')
    if incomes is None:
        incomes = []
        returnStr = returnStr + " OPTIONAL: incomes "
    shared_users = jsonObj.get('shared_users')
    if shared_users is None:
        shared_users = []
        returnStr = returnStr + " OPTIONAL: shared_users "
    settings = jsonObj.get('settings')
    if settings is None:
        settings = []
        returnStr = returnStr + " OPTIONAL: settings "
    if cur.execute("SELECT * FROM lists where list_name = '{}'".format(list_name)).fetchall() != []:
        return "list already exists. update instead from /api/users/(user_id)/lists/(list_id)"
    cur.execute("INSERT INTO lists VALUES ('{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
    list_name,
    list_id,
    user_id,
    username,
    json.dumps(categories),
    json.dumps(incomes),
    json.dumps(expenses),
    json.dumps(shared_users),
    json.dumps(settings)
    )
    )
    userLists = cur.execute("SELECT lists FROM users WHERE user_id = '{}'".format(user_id)).fetchall()[0][0]
    userLists = json.loads(userLists)
    userLists.append(list_id)
    cur.execute("UPDATE users set lists = '{}' WHERE user_id = '{}'".format(json.dumps(userLists), user_id))
    con.commit()
    return " List created. " + returnStr

@app.route('/api/users/<user_id>/friends', strict_slashes=False)
def displayUserFriends(user_id=None):
    '''displays info from SQLite about user'''
    response = cur.execute('SELECT friends FROM users WHERE user_id = "{}"'.format(user_id)).fetchall()
    if response != []:
        for r in response:
            dic = {r.keys()[i]: r[i] for i in range(len(r))}
        return (json.dumps(dic))
    else:
        return('user not found')

@app.route('/api/users/<user_id>/friends', strict_slashes=False, methods=['POST'])
def postUserFriends(user_id=None):
    '''This method creates a route and gives it some text'''
    request_content_type = rq.headers.get('Content-Type')
    if cur.execute("SELECT * FROM users where user_id = '{}'".format(user_id)).fetchall() == []:
        return "not a valid user_id"
    jsonObj = rq.json
    friends = jsonObj.get('friends')
    if friends is None:
        return "requires friends"
    else:
        cur.execute("UPDATE users SET friends = '{}' where user_id = '{}'".format(friends, user_id))
    con.commit()
    return json.dumps('set user {} friends to {}'.format(user_id, friends))

###########################################
@app.route('/api/users/<user_id>/friends', strict_slashes=False, methods=['PUT'])
def putUserFriends(user_id=None):
    return "not yet implemented"

@app.route('/api/users/<user_id>/settings', strict_slashes=False)
def displayUserSettings(user_id=None):
    '''displays info from SQLite about user'''
    response = cur.execute('SELECT settings FROM users WHERE user_id = "{}"'.format(user_id)).fetchall()
    if response != []:
        for r in response:
            dic = {r.keys()[i]: r[i] for i in range(len(r))}
        return (json.dumps(dic))
    else:
        return('user not found')

@app.route('/api/users/<user_id>/settings', strict_slashes=False, methods=['POST'])
def postUserSettings(user_id=None):
    '''This method creates a route and gives it some text'''
    request_content_type = rq.headers.get('Content-Type')
    if cur.execute("SELECT * FROM users where user_id = '{}'".format(user_id)).fetchall() == []:
        return "not a valid user_id"
    jsonObj = rq.json
    settings = jsonObj.get('settings')
    if settings is None:
        return "requires settings"
    else:
        cur.execute("UPDATE users SET settings = '{}' where user_id = '{}'".format(settings, user_id))
    con.commit()
    return json.dumps('set user {} settings to {}'.format(user_id, settings))

###########################################
@app.route('/api/users/<user_id>/settings', strict_slashes=False, methods=['PUT'])
def putUserSettings(user_id=None):
    return "not yet implemented"

@app.route('/api/users/<user_id>/lists/<list_id>', strict_slashes=False)
def displayUserList(user_id=None, list_id=None):
    '''displays info from SQLite about user'''
    response = cur.execute('SELECT * FROM lists WHERE owner_id = "{}" AND list_id = "{}"'.format(user_id, list_id)).fetchall()
    if response != []:
        for r in response:
            dic = {r.keys()[i]: r[i] for i in range(len(r))}
        return (json.dumps(dic))
    else:
        return('list not found')

@app.route('/api/users/<user_id>/lists/<list_id>', strict_slashes=False, methods=['POST'])
def postListUpdate(user_id=None, list_id=None):
    '''This method creates a route and gives it some text'''
    request_content_type = rq.headers.get('Content-Type')
    if cur.execute("SELECT * FROM users where user_id = '{}'".format(user_id)).fetchall() == []:
        return "not a valid user_id"
    if cur.execute("SELECT * FROM lists where list_id = '{}'".format(list_id)).fetchall() == []:
        return "not a valid list_id"
    jsonObj = rq.json
    returnStr = ""
    list_name = jsonObj.get('list_name')
    if list_name is None:
        returnStr = returnStr + " OPTIONAL: list_name "
    elif list_name.replace(" ", "") == "":
        return "list_name cannot be blank"
    else:
        cur.execute("UPDATE lists SET list_name = '{}' where list_id = '{}'".format(list_name, list_id))
    owner_id = jsonObj.get('owner_id')
    if owner_id is None:
        returnStr = returnStr + " OPTIONAL: owner_id (auto-updates owner_name) "
    else:
        username = cur.execute("SELECT username FROM users where user_id = '{}'".format(owner_id)).fetchall()[0][0]
        if username == []:
            returnStr = returnStr + " owner_id is not valid user_id. this value not updated. "
        else:
            cur.execute("UPDATE lists SET owner_id = '{}' where list_id = '{}'".format(owner_id, list_id))
            cur.execute("UPDATE lists SET owner_name = '{}' where list_id = '{}'".format(username, list_id))
    categories = jsonObj.get('categories')
    if categories is None:
        returnStr = returnStr + " OPTIONAL: categories "
    elif type(categories) != str:
        return 'categories is not valid json object (must be str)'
    else:
        cur.execute("UPDATE lists SET categories = '{}' where list_id = '{}'".format(categories, list_id))
    expenses = jsonObj.get('expenses')
    if expenses is None:
        returnStr = returnStr + " OPTIONAL: expenses "
    elif type(expenses) != str:
        return 'expenses is not valid json object (must be str)'
    else:
        cur.execute("UPDATE lists SET expenses = '{}' where list_id = '{}'".format(expenses, list_id))
    incomes = jsonObj.get('incomes')
    if incomes is None:
        returnStr = returnStr + " OPTIONAL: incomes "
    elif type(incomes) != str:
        return 'incomes is not valid json object (must be str)'
    else:
        cur.execute("UPDATE lists SET incomes = '{}' where list_id = '{}'".format(incomes, list_id))
    shared_users = jsonObj.get('shared_users')
    if shared_users is None:
        returnStr = returnStr + " OPTIONAL: shared_users "
    elif type(shared_users) != str:
        return 'incomes is not valid json object (must be str)'
    else:
        shared_users_obj = json.loads(shared_users)
        try:
            for user in shared_users_obj:
                uuid.UUID(user, version=4)
        except Exception:
            return "shared_users must be a list of valid uuid4"
        for user in shared_users_obj:
            if cur.execute("SELECT username FROM users WHERE user_id = '{}'".format(user)).fetchall() == []:
                return 'user_id not found: {}'.format(user)
        cur.execute("UPDATE lists SET shared_users = '{}' where list_id = '{}'".format(shared_users, list_id))
    settings = jsonObj.get('settings')
    if settings is None:
        returnStr = returnStr + " OPTIONAL: settings "
    elif type(settings) != str:
        return 'settings is not valid json object (must be str)'
    else:
        cur.execute("UPDATE lists SET settings = '{}' where list_id = '{}'".format(settings, list_id))
    con.commit()
    return " List updated (overwritten). " + returnStr

######################################
@app.route('/api/users/<user_id>/lists/<list_id>', strict_slashes=False, methods=['PUT'])
def putListUpdate(user_id=None, list_id=None):
    return "not yet implemented"

@app.route('/api/users/<user_id>/lists/<list_id>/name', strict_slashes=False)
def displayUserListName(user_id=None, list_id=None):
    '''displays info from SQLite about user'''
    response = cur.execute('SELECT list_name FROM lists WHERE owner_id = "{}" AND list_id = "{}"'.format(user_id, list_id)).fetchall()
    if response != []:
        for r in response:
            dic = {r.keys()[i]: r[i] for i in range(len(r))}
        return (json.dumps(dic))
    else:
        return('list not found')

@app.route('/api/users/<user_id>/lists/<list_id>/name', strict_slashes=False, methods=['POST'])
def postListNameUpdate(user_id=None, list_id=None):
    '''This method creates a route and gives it some text'''
    request_content_type = rq.headers.get('Content-Type')
    if cur.execute("SELECT * FROM users where user_id = '{}'".format(user_id)).fetchall() == []:
        return "not a valid user_id"
    if cur.execute("SELECT * FROM lists where list_id = '{}'".format(list_id)).fetchall() == []:
        return "not a valid list_id"
    jsonObj = rq.json
    list_name = jsonObj.get('list_name')
    if list_name is None:
        return "requires list_name"
    elif list_name.replace(" ", "") == "":
        return "list_name cannot be blank"
    else:
        cur.execute("UPDATE lists SET list_name = '{}' where list_id = '{}'".format(list_name, list_id))
    con.commit()
    return json.dumps('set list {} name to {}'.format(list_id, list_name))

@app.route('/api/users/<user_id>/lists/<list_id>/categories', strict_slashes=False)
def displayUserListCategories(user_id=None, list_id=None):
    '''displays info from SQLite about user'''
    response = cur.execute('SELECT categories FROM lists WHERE owner_id = "{}" AND list_id = "{}"'.format(user_id, list_id)).fetchall()
    if response != []:
        for r in response:
            dic = {r.keys()[i]: r[i] for i in range(len(r))}
        return (json.dumps(dic))
    else:
        return('list not found')

@app.route('/api/users/<user_id>/lists/<list_id>/categories', strict_slashes=False, methods=['POST'])
def postListCategoriesUpdate(user_id=None, list_id=None):
    '''This method creates a route and gives it some text'''
    request_content_type = rq.headers.get('Content-Type')
    if cur.execute("SELECT * FROM users where user_id = '{}'".format(user_id)).fetchall() == []:
        return "not a valid user_id"
    if cur.execute("SELECT * FROM lists where list_id = '{}'".format(list_id)).fetchall() == []:
        return "not a valid list_id"
    jsonObj = rq.json
    categories = jsonObj.get('categories')
    if categories is None:
        return "requires categories"
    else:
        cur.execute("UPDATE lists SET categories = '{}' where list_id = '{}'".format(categories, list_id))
    con.commit()
    return json.dumps('set list {} categories to {}'.format(list_id, categories))

###########################################
@app.route('/api/users/<user_id>/lists/<list_id>/categories', strict_slashes=False, methods=['PUT'])
def putListCategoriesUpdate(user_id=None, list_id=None):
    return "not yet implemented"



@app.route('/api/users/<user_id>/lists/<list_id>/expenses', strict_slashes=False)
def displayUserListExpenses(user_id=None, list_id=None):
    '''displays info from SQLite about user'''
    response = cur.execute('SELECT expenses FROM lists WHERE owner_id = "{}" AND list_id = "{}"'.format(user_id, list_id)).fetchall()
    if response != []:
        for r in response:
            dic = {r.keys()[i]: r[i] for i in range(len(r))}
        return (json.dumps(dic))
    else:
        return('list not found')

@app.route('/api/users/<user_id>/lists/<list_id>/expenses', strict_slashes=False, methods=['POST'])
def postListExpensesUpdate(user_id=None, list_id=None):
    '''This method creates a route and gives it some text'''
    request_content_type = rq.headers.get('Content-Type')
    if cur.execute("SELECT * FROM users where user_id = '{}'".format(user_id)).fetchall() == []:
        return "not a valid user_id"
    if cur.execute("SELECT * FROM lists where list_id = '{}'".format(list_id)).fetchall() == []:
        return "not a valid list_id"
    jsonObj = rq.json
    expense_amount = jsonObj.get('expense_amount')
    if expense_amount is None:
        return "requires expense_amount"
    expense_name = jsonObj.get('expense_name')
    if expense_name is None:
        return "requires expense_name"
    expense_description = jsonObj.get('expense_description')
    if expense_description is None:
        return "requires expense_description"
    exp_list = cur.execute("SELECT expenses FROM lists where list_id = '{}'".format(list_id)).fetchall()[0][0]
    exp_list = json.loads(exp_list)
    exp_list.append([str(uuid.uuid4()), float(expense_amount), expense_name, expense_description])
    cur.execute("UPDATE lists SET expenses = '{}' where list_id = '{}'".format(json.dumps(exp_list), list_id))
    con.commit()
    return json.dumps('set list {} expenses to {}'.format(list_id, exp_list))

@app.route('/api/users/<user_id>/lists/<list_id>/expenses/<expense_id>', strict_slashes=False)
def displayUserListExpensesID(user_id=None, list_id=None, expense_id=None):
    '''displays info from SQLite about user'''
    if cur.execute("SELECT * FROM users where user_id = '{}'".format(user_id)).fetchall() == []:
        return "not a valid user_id"
    if cur.execute("SELECT * FROM lists where list_id = '{}'".format(list_id)).fetchall() == []:
        return "not a valid list_id"
    exp_list = cur.execute("SELECT expenses FROM lists where list_id = '{}'".format(list_id)).fetchall()[0][0]
    exp_list = json.loads(exp_list)
    for li in exp_list:
        if expense_id in li:
            return json.dumps(li)
    return "expense not found"

############################################
@app.route('/api/users/<user_id>/lists/<list_id>/expenses/<expense_id>', strict_slashes=False, methods=['PUT'])
def PostUserListExpensesID(user_id=None, list_id=None, expense_id=None):
    '''displays info from SQLite about user'''
    return "Not yet implemented"

@app.route('/api/users/<user_id>/lists/<list_id>/incomes', strict_slashes=False)
def displayUserListIncomes(user_id=None, list_id=None):
    '''displays info from SQLite about user'''
    response = cur.execute('SELECT incomes FROM lists WHERE owner_id = "{}" AND list_id = "{}"'.format(user_id, list_id)).fetchall()
    if response != []:
        for r in response:
            dic = {r.keys()[i]: r[i] for i in range(len(r))}
        return (json.dumps(dic))
    else:
        return('list not found')

@app.route('/api/users/<user_id>/lists/<list_id>/incomes', strict_slashes=False, methods=['POST'])
def postListIncomesUpdate(user_id=None, list_id=None):
    '''This method creates a route and gives it some text'''
    request_content_type = rq.headers.get('Content-Type')
    if cur.execute("SELECT * FROM users where user_id = '{}'".format(user_id)).fetchall() == []:
        return "not a valid user_id"
    if cur.execute("SELECT * FROM lists where list_id = '{}'".format(list_id)).fetchall() == []:
        return "not a valid list_id"
    jsonObj = rq.json
    income_amount = jsonObj.get('income_amount')
    if income_amount is None:
        return "requires income_amount"
    income_name = jsonObj.get('income_name')
    if income_name is None:
        return "requires income_name"
    income_description = jsonObj.get('income_description')
    if income_description is None:
        return "requires income_description"
    inc_list = cur.execute("SELECT incomes FROM lists where list_id = '{}'".format(list_id)).fetchall()[0][0]
    inc_list = json.loads(inc_list)
    inc_list.append([str(uuid.uuid4()), float(income_amount), income_name, income_description])
    cur.execute("UPDATE lists SET incomes = '{}' where list_id = '{}'".format(json.dumps(inc_list), list_id))
    con.commit()
    return json.dumps('set list {} incomes to {}'.format(list_id, inc_list))

@app.route('/api/users/<user_id>/lists/<list_id>/incomes/<income_id>', strict_slashes=False)
def displayUserListIncomesID(user_id=None, list_id=None, income_id=None):
    '''displays info from SQLite about user'''
    if cur.execute("SELECT * FROM users where user_id = '{}'".format(user_id)).fetchall() == []:
        return "not a valid user_id"
    if cur.execute("SELECT * FROM lists where list_id = '{}'".format(list_id)).fetchall() == []:
        return "not a valid list_id"
    inc_list = cur.execute("SELECT incomes FROM lists where list_id = '{}'".format(list_id)).fetchall()[0][0]
    inc_list = json.loads(inc_list)
    for li in inc_list:
        if income_id in li:
            return json.dumps(li)
    return "income not found"

############################################
@app.route('/api/users/<user_id>/lists/<list_id>/incomes/<income_id>', strict_slashes=False, methods=['PUT'])
def PostUserListIncomesID(user_id=None, list_id=None, income_id=None):
    '''displays info from SQLite about user'''
    return "Not yet implemented"

@app.route('/api/users/<user_id>/lists/<list_id>/shared_users', strict_slashes=False)
def displayUserListUsers(user_id=None, list_id=None):
    '''displays info from SQLite about user'''
    response = cur.execute('SELECT shared_users FROM lists WHERE owner_id = "{}" AND list_id = "{}"'.format(user_id, list_id)).fetchall()
    if response != []:
        for r in response:
            dic = {r.keys()[i]: r[i] for i in range(len(r))}
        return (json.dumps(dic))
    else:
        return('list not found')

@app.route('/api/users/<user_id>/lists/<list_id>/shared_users', strict_slashes=False, methods=['POST'])
def postListSharedUsersUpdate(user_id=None, list_id=None):
    '''This method creates a route and gives it some text'''
    request_content_type = rq.headers.get('Content-Type')
    if cur.execute("SELECT * FROM users where user_id = '{}'".format(user_id)).fetchall() == []:
        return "not a valid user_id"
    if cur.execute("SELECT * FROM lists where list_id = '{}'".format(list_id)).fetchall() == []:
        return "not a valid list_id"
    jsonObj = rq.json
    shared_users = jsonObj.get('shared_users')
    if shared_users is None:
        return "requires shared_users"
    elif type(shared_users) != str:
        return 'incomes is not valid json object (must be str)'
    else:
        try:
            shared_users_obj = json.loads(shared_users)
        except Exception:
            return "shared_users is not valid json object"
        try:
            for user in shared_users_obj:
                uuid.UUID(user, version=4)
        except Exception:
            return "shared_users must be a list of valid uuid4"
        for user in shared_users_obj:
            if cur.execute("SELECT username FROM users WHERE user_id = '{}'".format(user)).fetchall() == []:
                return 'user_id not found: {}'.format(user)
        cur.execute("UPDATE lists SET shared_users = '{}' where list_id = '{}'".format(shared_users, list_id))
        con.commit()
        return 'set list {} shared_users to {}'.format(list_id, shared_users)

###########################################
@app.route('/api/users/<user_id>/lists/<list_id>/shared_users', strict_slashes=False, methods=['PUT'])
def putListSharedUsersUpdate(user_id=None, list_id=None):
    return "not yet implemented"

@app.route('/api/users/<user_id>/lists/<list_id>/list_settings', strict_slashes=False)
def displayUserListSettings(user_id=None, list_id=None):
    '''displays info from SQLite about user'''
    response = cur.execute('SELECT settings FROM lists WHERE owner_id = "{}" AND list_id = "{}"'.format(user_id, list_id)).fetchall()
    if response != []:
        for r in response:
            dic = {r.keys()[i]: r[i] for i in range(len(r))}
        return (json.dumps(dic))
    else:
        return('list not found')

@app.route('/api/users/<user_id>/lists/<list_id>/list_settings', strict_slashes=False, methods=['POST'])
def postListSettingsUpdate(user_id=None, list_id=None):
    '''This method creates a route and gives it some text'''
    request_content_type = rq.headers.get('Content-Type')
    if cur.execute("SELECT * FROM users where user_id = '{}'".format(user_id)).fetchall() == []:
        return "not a valid user_id"
    if cur.execute("SELECT * FROM lists where list_id = '{}'".format(list_id)).fetchall() == []:
        return "not a valid list_id"
    jsonObj = rq.json
    list_settings = jsonObj.get('list_settings')
    if list_settings is None:
        return "requires list_settings"
    else:
        cur.execute("UPDATE lists SET settings = '{}' where list_id = '{}'".format(list_settings, list_id))
    con.commit()
    return json.dumps('set list {} settings to {}'.format(list_id, list_settings))

###########################################
@app.route('/api/users/<user_id>/lists/<list_id>/list_settings', strict_slashes=False, methods=['PUT'])
def putListSettingsUpdate(user_id=None, list_id=None):
    return "not yet implemented"

"""
PUSH request for:
/api/users/<user_id>/lists/<list_id>/expenses/<expense_id>
/api/users/<user_id>/lists/<list_id>/incomes/<income_id>

PUT request for:
/api/users/<user_id> (friends and settings)
/api/users/<user_id>/lists
/api/users/<user_id>/friends
/api/users/<user_id>/settings
/api/users/<user_id>/lists/<list_id>
/api/users/<user_id>/lists/<list_id>/categories
/api/users/<user_id>/lists/<list_id>/expenses
/api/users/<user_id>/lists/<list_id>/incomes
/api/users/<user_id>/lists/<list_id>/shared_users
/api/users/<user_id>/lists/<list_id>/list_settings
"""






if __name__ == '__main__':
    '''this method sets everything to work on 0.0.0.0'''
    #app.debug = True
    app.run(host='0.0.0.0', port=5000)
