#Moduler fra flask
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

import json

app = Flask(__name__)


users= []


def updateJson():
    with open('users.json','w+') as usersfile:
        usersfile.write(json.dumps(users))
def fixShitPlease():
    for i, thing in enumerate(users):
        thing["id"]=i
    #global varer
    #varer = varer[:]
    updateJson()

def validate_user(username, password):
    for user in users:
        if user['un'] == username and user['pw'] == password:
            return True
    return False

def check_used_username(username, email):
    for user in users:
        if user['un'] == username or user['em'] == email:
            return True
    return False

     
try:
    with open('users.json','r') as usersfile:
        users = json.load(usersfile)
        fixShitPlease()

except:
    print("File did not have relevant information")
    users = []



@app.route("/")
def index():
    return render_template("frontpage.html", users = users)


@app.route("/admin_user_change", methods=["post", "get"])
def add_new():
    if request.method == 'POST':
        try:
            createordestroy = request.form["action"]
            un = request.form['username']
            pw = request.form['password']
            em = request.form['email']
        except:
            return redirect("/")
        try:
            id = request.form['userid']
        except:
            id = "0"
            
        
        
        #Ret/rediger en vare
        if createordestroy == "change":
            id = int(id)
            if id > len(users):
                print("How den varer fandtes ikke!!")
                return redirect("/")
            user = {'id': id, 'em': em, 'un': un, 'pw': pw}
            users[id] = user
            print(f"Users: {users}")
            fixShitPlease()
            return redirect("/")
        
        #Lav en ny vare
        elif createordestroy == "create":
            user = {'id': len(users), 'em': em, 'un': un, 'pw': pw}
            users.append(user)
            print(f"Users: {users}")
            fixShitPlease()
            return redirect("/")
        
        #Slet varen
        else:
            print("destroy", id)
            del users[int(id)]
            fixShitPlease()
            return redirect("/")
    else:
        return render_template("adminchangeusers.html", users = users )
    
@app.route("/createuser", methods=["post", "get"])
def createuser():
    if request.method == 'POST':
        try:
            un = request.form['username']
            pw = request.form['password']
            em = request.form['email']
        except:
            return redirect("/")
        try:
            id = request.form['userid']
        except:
            id = "0"
        
        if not check_used_username(un, em):
            user = {'id': len(users),'em': em, 'un': un, 'pw': pw}
            users.append(user)
            print(f"Users: {users}")
            fixShitPlease()
            return redirect("/")  
        else: return render_template("createnewuser.html", username_or_email_exists = True, users = users)
            
    else:
        return render_template("createnewuser.html", users = users )



@app.route("/login", methods=["post", "get"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if validate_user(username, password):
            return redirect("/")# Du kan ændre denne del til at omdirigere brugeren til en anden side efter vellykket login.
        else:
            return render_template("login.html", failure = True)  # Du kan vise en besked om, at login mislykkedes.

    return render_template("login.html", users=users, failure = False)


if __name__ == "__main__":
    app.run(debug=True, port=6002)