from flask import Flask, render_template, redirect, session
from flask_wtf import FlaskForm
from wtforms import StringField
import random
import requests

app = Flask(__name__)
app.debug = True
app.secret_key = "2asd§ůkvndopsnfiasda askdaopf 114"
API_KEY ="bfa5fe8e44043ff04582011d9707f5ee"

class polohaForm(FlaskForm):
    poloha = StringField() 

@app.route('/',methods=['GET','POST'])
def poloha():
    form = polohaForm()
    poloha = form.poloha.data
    if form.validate_on_submit():
        session["poloha"] = poloha # ulozim informaci do prohlizece, takze to muzu pouzit i v ("/")
        return redirect("/poloha")
    return render_template("poloha.html", form=form)

@app.route('/poloha',methods=['GET','POST'])
def pocasi():
    misto = session['poloha']
    url = f'https://api.openweathermap.org/data/2.5/weather?q={misto}&appid={API_KEY}&lang=cz&units=metric' # fstring  
    odpoved = requests.get(url).json()
    teplota = odpoved['main']['temp'] # nemusime, protoze to neni pole v pole
    popis = odpoved['weather'][0]['description'] # musime [0] abychom vytahli z prvky z pole (je to pole v poli)
    pocitova = odpoved['main']['feels_like']
    zeme = odpoved['sys']['country']
    return render_template('index.html',odpoved=odpoved, teplota=teplota, popis=popis, pocitova = pocitova,zeme=zeme,misto=misto)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
