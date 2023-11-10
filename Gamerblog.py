#Moduler fra flask
from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)

app.secret_key = 'your_secret_key'  # Dette skal være en stærk og unik nøgle


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

def check_used_username_or_email(username, email):
    for user in users:
        if user['un'] == username or user['em'] == email:
            return True
    return False

def validate_email(email):
    for user in users:
        if user['em'] == email:
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
            
        
        
        #Ret/rediger en konto
        if createordestroy == "change":
            id = int(id)
            users[id]['email'] = em
            users[id]['username'] = un
            users[id]['password'] = pw
            if id > len(users):
                print("Hov den varer fandtes ikke!!")
                return redirect("/")

            #elif not check_used_username_or_email(un, em):
            #    user = {'id': len(users),'em': em, 'un': un, 'pw': pw}
            #    users[id] = user
            #    print(f"Users: {users}")
            #    fixShitPlease()
            #    return redirect("/") 
            else: return render_template("adminchangeusers.html", username_or_email_exists = True, users = users) 
        
        #Lav en ny konto
        elif createordestroy == "create":
            if not check_used_username_or_email(un, em):
                user = {'id': len(users),'em': em, 'un': un, 'pw': pw}
                users.append(user)
                print(f"Users: {users}")
                fixShitPlease()
                return redirect("/")
            else: return render_template("adminchangeusers.html", username_or_email_exists = True, users = users)  
        
        #Slet en konto
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
            email = request.form['email']
        except:
            return redirect("/")
        try:
            id = request.form['userid']
        except:
            id = "0"
        
        if not check_used_username_or_email(un, em):
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
        session['username'] = request.form['username']

        if validate_user(username, password):
            session['logged_in'] = True
            admin_usernames = ['Vedad', 'Linus']
            session['admin'] = True if username in admin_usernames else False
            return redirect("/")
        else:
            return render_template("login.html", failure=True)

    return render_template("login.html", users=users, failure=False)

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.clear()
    return redirect("/")


@app.route("/login/forgottenPassword", methods=["post", "get"])
def forgotten_password():
    if request.method == 'POST':
        email = request.form['email']
        newpassword = request.form['newpassword']
        confirm = request.form['confirmpassword']

        if newpassword == confirm:
            if validate_email(email):
                for user in users:
                    if user['em'] == email:  # Find the user by email
                        user['pw'] = newpassword  # Update the password
                print(f"Users: {users}")
                fixShitPlease()
                return redirect("/login")  
                # Du kan ændre denne del til at omdirigere brugeren til en anden side efter vellykket login.
            else:
                return render_template("forgotten.html", failure = True)  # Du kan vise en besked om, at login mislykkedes.
    return render_template("forgotten.html", users=users, failure = False)


if __name__ == "__main__":
    app.run(debug=True, port=6002)