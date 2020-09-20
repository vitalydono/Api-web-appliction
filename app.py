import requests
from flask import Flask, render_template,url_for,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#from models import Todo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    def __repr__(self):
        return '<Task %r>' % self.id

db.create_all()


@app.route('/', methods =["POST","GET"])
def index():

    #city = "Beer sheva"

    if request.method == "POST":
        new_city = request.form.get("city")
        if new_city != "":
            cityobj = City(name=new_city)

            db.session.add(cityobj)
            db.session.commit()


    cities = City.query.all()

    # db.session.query(City).delete()
    # db.session.commit()


    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=5cecc4d745c9bdcd72bbb2e8b58f4c61"

    weather_data = []
    for city in cities:
        r = requests.get(url.format(city.name)).json()

        print(r)

        weather = {
            "city": city.name,
            "temperature": r["main"]["temp"],
            "description": r["weather"][0]["description"],
            "icon": r["weather"][0]["icon"]
        }
        weather_data.append(weather)
    return render_template("index.html", weather_data=weather_data)

if __name__ == "__main__":
    app.run(debug=True)
