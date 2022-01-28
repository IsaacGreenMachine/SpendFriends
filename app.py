#!/usr/bin/python3
'''
this script creates a page to return hello hbnb
'''
from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/', strict_slashes=False)
@app.route('/overview', strict_slashes=False)
def homePage():
    '''This method creates a route and gives it some text'''
    return render_template('overview.html')

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

@app.route('/loginPage', strict_slashes=False)
def loginPage():
    '''This method creates a route and gives it some text'''
    return render_template('loginPage.html')

if __name__ == '__main__':
    '''this method sets everything to work on 0.0.0.0'''
    #app.debug = True
    app.run(host='0.0.0.0', port=5000)
