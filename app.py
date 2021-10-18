from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Travel_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    city_depart = db.Column(db.String(200), nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    interest = db.Column(db.Integer, nullable=False)  # list

@app.route('/')
def index():
    data = Travel_Data.query.all()
    return render_template('index.html', data=data)

#  db.create_all()
#  intialize()

if __name__ == '__main__':
    app.run(debug=True)

