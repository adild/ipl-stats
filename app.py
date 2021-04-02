from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Password'

class InputForm(FlaskForm):
	playername = StringField('playername', validators=[DataRequired()])
	team2 =  StringField('team2', validators=[DataRequired()])
	language = SelectField(u'Programming Language', validate_choice=False)
	submit = SubmitField('Search')

@app.route('/form', methods=['GET', 'POST'])
def form():
	form = InputForm()

	if form.validate_on_submit():
		return redirect('/form')

	return render_template('form.html', form=form)

if __name__ == '__main__':
	app.run(debug=True)
