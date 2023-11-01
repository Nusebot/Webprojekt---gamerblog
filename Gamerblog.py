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
        

try:
    with open('users.json','r') as usersfile:
        users = json.load(usersfile)
        fixShitPlease()

except:
    print("Filen havde ikke relevant indhold")
    users = []



@app.route("/")
def index():
    return render_template("index.html", users = users)


@app.route("/add_new", methods=["post", "get"])
def add_new():
    if request.method == 'POST':
        try:
            skabellerslet = request.form["action"]
            navn = request.form['produkt_navn']
            pris = request.form['produkt_pris']
        except:
            return redirect("/")
        try:
            id = request.form['vareid']
        except:
            id = "0"
            
        
        
        #Ret/rediger en vare
        if skabellerslet == "rediger":
            id = int(id)
            if id > len(users):
                print("How den varer fandtes ikke!!")
                return redirect("/")
            user = {'id': id, 'un':pris, 'pw': navn}
            users[id] = user
            print(f"Users: {users}")
            fixShitPlease()
            return redirect("/")
        
        #Lav en ny vare
        elif skabellerslet == "skab":
            user = {'id': len(users), 'un':pris, 'pw': navn}
            users.append(user)
            print(f"Users: {users}")
            fixShitPlease()
            return redirect("/")
        
        #Slet varen
        else:
            print("slet", id)
            del users[int(id)]
            fixShitPlease()
            return redirect("/")
    else:
        return render_template("add_new.html", users = users )

if __name__ == "__main__":
    app.run(debug=True, port=6002)