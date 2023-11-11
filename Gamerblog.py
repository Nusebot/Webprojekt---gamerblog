#Moduler fra flask
from flask import Flask, render_template, request, redirect, session, flash
import json
from datetime import timedelta, datetime 
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

def check_used_username_or_email(username, email, exclude_user_id=None):
    for user in users:
        if user['id'] != exclude_user_id and (user['un'] == username or user['em'] == email):
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
            
        
        
        # Ret/rediger en konto
        if createordestroy == "change":
            id = int(id)
    
            # Check if the provided email corresponds to the user's email
            if users[id]['em'] == em:
                # Check if the new email is already used (excluding the current user)
                if not check_used_username_or_email(un, em, exclude_user_id=id):
                    # Update the user's information
                    users[id]['em'] = em
                    users[id]['un'] = un
                    users[id]['pw'] = pw

                    fixShitPlease()
                    return redirect("/") 
                else:
                    # Render template with a message about other users using the new username or email
                    return render_template("adminchangeusers.html", username_or_email_exists=True, users=users)
            else:
                # Render template with a message about incorrect email
                return render_template("adminchangeusers.html", incorrect_email=True, users=users)


        
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

# Function to check if the user is logged in and update the last activity time
def check_login_status():
    if 'logged_in' in session:
        session['last_activity'] = datetime.now()


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20)
    session.modified = True
    check_login_status()

    # Check for inactivity and log out if the time has passed
    if 'last_activity' in session:
        inactive_duration = datetime.now() - session['last_activity']
        if inactive_duration > timedelta(minutes=20):
            session.clear()
            flash('You have been logged out due to inactivity.', 'info')
            return redirect("/login")


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
            session.permanent = False  # Set session to expire when the browser is closed
            return redirect("/")
        else:
            return render_template("login.html", failure=True)

    return render_template("login.html", users=users, failure=False)

@app.route("/logout")
def logout():
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