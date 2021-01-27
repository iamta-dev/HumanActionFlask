from flask import Flask , render_template ,request,redirect

app=Flask(__name__)
app.debug = True

import requests
class HumanAction():
    def getHumanAction(self):
        URL='http://localhost:5000/human-action/'
        response=requests.get(URL)
        objs=response.json()
        return objs

hA = HumanAction()

@app.route("/")
def viewIndex():
    return render_template('index.html',objs = hA.getHumanAction())

@app.route("/add")
def viewAdd():
    return render_template('add.html',objs = hA.getHumanAction())

if __name__=="__main__":
    app.run(debug=True, port=8080)