from flask import Flask, render_template, redirect, url_for, request
from datetime import  datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # criando o app
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # instanciando banco de dados


class Food(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	protein = db.Column(db.Integer,  nullable=False)
	carbo = db.Column(db.Integer,  nullable=False)
	fat = db.Column(db.Integer,  nullable=False)
	calories = db.Column(db.Integer, nullable=False)

	diets = db.relationship('Diet', backref='food', lazy='dynamic')

	def __repr__(self):
		return 'Food: %r '% self.name


class Diet(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.Date)
	food_id = db.Column(db.Integer, db.ForeignKey('food.id'))


@app.route('/')
def index():
	
	dieta = Diet.query.order_by(Diet.date).all()
	
	return render_template('home.html', dieta= dieta)


@app.route('/day', methods=['GET','POST'])
def day():
	if request.method == 'POST':
		data = request.form['data']
		
		dt = datetime.strptime(data, '%Y-%m-%d')
		dtformat = datetime.strftime(dt, '%d%m%Y')
		
		day = int(dtformat[0:2])
		month= int(dtformat[2:4])
		year = int(dtformat[4:12])
		
		data_final = datetime(year,month,day)

		item = request.form['food-select']
		
		diet = Diet(date=data_final, food_id=item)
		db.session.add(diet)
		db.session.commit()
		return redirect(url_for('index'))
			
	food = Food.query.all()
	
	return render_template('day.html', food=food)


@app.route('/food', methods=['GET', 'POST'])
def food():
	if request.method == 'POST':
		food = request.form['food-name']
		protein = int(request.form['protein'])
		carbo = int(request.form['carbo'])
		fat = int(request.form['fat'])
		calories = (protein * 4) + (carbo * 4) +(fat * 9)

		item = Food(name=food, protein=protein, carbo=carbo, fat=fat, calories=calories)
		db.session.add(item)
		db.session.commit()
	foods = Food.query.all()	
	return render_template('food.html', foods=foods)


if __name__ == '__main__':
	app.run(debug=True)
