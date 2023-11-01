#Moduler fra flask
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

import json

app = Flask(__name__)


varer = []


def updateJson():
    with open('varer.json','w+') as varefil:
        varefil.write(json.dumps(varer))
def fixShitPlease():
    for i, thing in enumerate(varer):
        thing["id"]=i
    #global varer
    #varer = varer[:]
    updateJson()
        

try:
    with open('varer.json','r') as varefil:
        varer = json.load(varefil)
        fixShitPlease()

except:
    print("Filen havde ikke relevant indhold")
    varer = []



@app.route("/")
def index():
    return render_template("index.html", varer = varer)

@app.route("/buy")
def buy():
    item = int(request.args['item'])
    return render_template("buy.html", vare=varer[item])
    


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
            if id > len(varer):
                print("How den varer fandtes ikke!!")
                return redirect("/")
            vare = {'id': id, 'pris':pris, 'navn': navn}
            varer[id] = vare
            print(f"Varer: {varer}")
            fixShitPlease()
            return redirect("/")
        
        #Lav en ny vare
        elif skabellerslet == "skab":
            vare = {'id': len(varer), 'pris':pris, 'navn': navn}
            varer.append(vare)
            print(f"Varer: {varer}")
            fixShitPlease()
            return redirect("/")
        
        #Slet varen
        else:
            print("slet", id)
            del varer[int(id)]
            fixShitPlease()
            return redirect("/")
    else:
        return render_template("add_new.html", varer = varer )

if __name__ == "__main__":
    app.run(debug=True, port=6002)