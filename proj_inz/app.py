from flask import Flask,request,render_template, url_for, redirect, flash
import requests, time
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pogoda.db'
app.config['SECRET_KEY'] = 'sekretnyklucz'
db = SQLAlchemy(app)

class City(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)

def pogoda_get(city):
	url = f'https://api.openweathermap.org/data/2.5/weather?q={ city }&units=metric&lang=pl&appid=df0702a285b4d6f03eb1e7517ee63026'
	odp = requests.get(url).json()
	return odp

def pogoda_getf(city):
	url = f'https://api.openweathermap.org/data/2.5/weather?q={ city }&units=imperial&lang=pl&appid=df0702a285b4d6f03eb1e7517ee63026'
	odp = requests.get(url).json()
	return odp

@app.route("/", methods=['GET']) 
@app.route("/cel", methods=['GET']) 
def indexget():
	
	miasta = City.query.all()
	
		
	pogoda_dane = []

	for city in miasta:

		odp = pogoda_get(city.name)
		

		pogoda = {
			'city' : city.name,
			'country' : odp['sys']['country'],
			'date' : time.strftime('%d/%m/%y %H:%M',time.gmtime(odp['dt'] +odp['timezone'])),
			'temperature' : odp['main']['temp'],
			'description' : odp['weather'][0]['description'],
			'icon' : odp['weather'][0]['icon'],
			'sunrise' : time.strftime('%H:%M',time.gmtime(odp['sys']['sunrise'] +odp['timezone'])),
			'sunset' : time.strftime('%H:%M',time.gmtime(odp['sys']['sunset'] +odp['timezone'])),
			'pressure': odp['main']['pressure'],
          	'wind': odp['wind']['speed'],

		}

		pogoda_dane.append(pogoda)

	return render_template('cel.html', pogoda_dane=pogoda_dane)




@app.route("/", methods=['POST']) 
@app.route("/cel", methods=['POST']) 
def indexpost():
	error = ''
	nowe_miasto = request.form.get('city')

	if nowe_miasto:
		istnieje = City.query.filter_by(name=nowe_miasto).first()
		if not istnieje:
			spr = pogoda_get(nowe_miasto)
			if spr['cod'] == 200:
				nowe_miasto_obj = City(name=nowe_miasto)

				db.session.add(nowe_miasto_obj)
				db.session.commit()
				success = 'Miasto zostało dodane'

			else:
				error = 'Miasto nie istnieje'
		else:
			error = 'Miasto już istnieje'
	if error:
		flash(error, 'danger')
	else:
		flash(success, 'success')
	
	return redirect(url_for('indexget'))


@app.route('/cel/usun/<name>')
@app.route('/usun/<name>')
def usun( name ):
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()

    flash(f'Usunięto { city.name }!', 'success')
    return redirect(url_for('indexget'))

@app.route('/usun/<name>')
@app.route('/fahr/usun/<name>')
def usunf( name ):
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()

    flash(f'Usunięto { city.name }!', 'success')
    return redirect(url_for('indexgetf'))



@app.route("/fahr", methods=['GET']) 
def indexgetf():
	
	miasta = City.query.all()
	
		
	pogoda_dane = []

	for city in miasta:

		odp = pogoda_getf(city.name)
		

		pogoda = {
			'city' : city.name,
			'country' : odp['sys']['country'],
			'date' : time.strftime('%d/%m/%y %H:%M',time.gmtime(odp['dt'] +odp['timezone'])),
			'temperature' : odp['main']['temp'],
			'description' : odp['weather'][0]['description'],
			'icon' : odp['weather'][0]['icon'],
			'sunrise' : time.strftime('%H:%M',time.gmtime(odp['sys']['sunrise'] +odp['timezone'])),
			'sunset' : time.strftime('%H:%M',time.gmtime(odp['sys']['sunset'] +odp['timezone'])),
			'pressure': odp['main']['pressure'],
          	'wind': odp['wind']['speed'],

		}

		pogoda_dane.append(pogoda)

	return render_template('fahr.html', pogoda_dane=pogoda_dane)




@app.route("/", methods=['POST']) 
@app.route("/fahr", methods=['POST']) 
def indexpostf():
	error = ''
	nowe_miasto = request.form.get('city')

	if nowe_miasto:
		istnieje = City.query.filter_by(name=nowe_miasto).first()
		if not istnieje:
			spr = pogoda_get(nowe_miasto)
			if spr['cod'] == 200:
				nowe_miasto_obj = City(name=nowe_miasto)

				db.session.add(nowe_miasto_obj)
				db.session.commit()
				success = 'Miasto zostało dodane'

			else:
				error = 'Miasto nie istnieje'
		else:
			error = 'Miasto już istnieje'
	if error:
		flash(error, 'danger')
	else:
		flash(success, 'success')
	
	return redirect(url_for('indexgetf'))




if __name__ == "__main__" : 
	app.run(debug=True) 