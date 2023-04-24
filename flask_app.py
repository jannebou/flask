from flask import Flask, render_template, request
import json
import sqlite3


app = Flask(__name__)

con = sqlite3.connect("mittaukset.db3")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS mittaukset (id INTEGER PRIMARY KEY, paiva INTEGER, mittaus INTEGER)")
con.commit()
con.close() 

lampotilat = [
    {'x':1, 'y':14},
    {'x':2, 'y':10},
    {'x':3, 'y':15}
]

paivat = [
    'Maanantai',
    'Tiistai',
    'Keskiviikko',
    'Torstai',
    'Perjantai',
    'Lauantai',
    'Sunnuntai',
    ]

@app.route('/api', methods=['GET'])
def index():
    return render_template("mittaukset.html")

@app.route('/lisaa', methods=['POST'])
def lisaa():
    uusimittaus = request.get_json(force=True)
    lampotilat.append(uusimittaus)
    return(json.dumps(uusimittaus))

@app.route('/lisaakantaan', methods=['POST'])
def lisaa_kantaan():
    uusimittaus = request.get_json(force=True)

    con = sqlite3.connect("mittaukset.db3")
    cur = con.cursor()
    cur.execute("INSERT INTO mittaukset (paiva, mittaus) VALUES (?,?)", [uusimittaus["x"]], [uusimittaus["y"]])
    con.commit()
    con.close()

    return(json.dumps(uusimittaus))

@app.route('/haekannasta', methods=['GET'])
def hae_kannasta():
    con = sqlite3.connect("mittaukset.db3")
    cur = con.cursor()
    cur.execute("SELECT paiva, mittaus FROM mittaukset")
    
    tiedot = cur.fetchall()
    kantatiedot = list()

    for paiva in tiedot:
        temp = dict(x=paiva[0], y=paiva[1])
        kantatiedot.append(temp)
    
    con.commit()
    con.close()

    return render_template("mittaukset.html", taulukko=kantatiedot, paivat=paivat)

if __name__ == "__main__":
    app.run(debug=True)