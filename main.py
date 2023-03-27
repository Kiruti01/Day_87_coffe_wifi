from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fds543jr5tua4543f543j5klSihBXox7C0sKR6b'
Bootstrap(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
db = SQLAlchemy(app)


class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    map_url = StringField("Cafe Location on Google Maps (URL)", validators=[DataRequired(), URL()])
    img_url = StringField("Main image of Cafe (URL)", validators=[DataRequired(), URL()])
    location = StringField("Location of Cafe", validators=[DataRequired()])
    seats = StringField("No of Seats", validators=[DataRequired()])
    coffee_price = StringField("Coffee Price(£)", validators=[DataRequired()])
    has_sockets = BooleanField("Sockets Availability?")
    has_toilet = BooleanField("Toilets Availability?")
    has_wifi = BooleanField("Wifi Availability?")
    can_take_calls = BooleanField("Calls Allowed?")
    submit = SubmitField('Submit')


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'<cafe {self.name}>'


@app.route("/")
def home():
    list_of_rows = Cafe.query.all()
    return render_template("index.html", cafes=list_of_rows)


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price="£"+form.coffee_price.data
        )
        try:
            db.session.add(new_cafe)
            db.session.commit()
        except:
            return "There is some error in saving Cafe to Database"

        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    list_of_rows = Cafe.query.all()
    return render_template('cafes.html', cafes=list_of_rows)


@app.route('/delete/<int:cafe_id>')
def delete_cafe(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect('/cafes')


if __name__ == '__main__':
    app.run(debug=True)
