from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import json
import pandas as pd

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'Password'

# class InputForm(FlaskForm):
# 	playername = StringField('playername', validators=[DataRequired()])
# 	team2 =  StringField('team2', validators=[DataRequired()])
# 	language = SelectField(u'Programming Language', validate_choice=False)
# 	submit = SubmitField('Search')

@app.route('/form', methods=['GET', 'POST'])
def form():

	if form.is_valid():
		

		inputPlayer = request.form.get("playerName")
		inputTeam = request.form.get("AgainstTeam")

		ball_df = pd.read_csv('data/IPL Ball-by-Ball 2008-2020.csv')
		match_df = pd.read_csv('data/IPL Matches 2008-2020.csv')

		filt = (ball_df['batsman'] == inputPlayer) \
		& (ball_df['bowling_team'] == inputTeam) \
		& ((ball_df['extras_type'] == 'noballs') | ((pd.isna(ball_df['extras_type']))))

		batsmanAgainstTeam = ball_df.loc[filt]

		merge_result = batsmanAgainstTeam.merge(match_df, how='inner', on='id')

		res = merge_result.groupby(
	        ['id']
	    ).agg(
	        batman = ('batsman', 'unique'),
	        team_playing = ('batting_team', 'unique'),
	        against = ('bowling_team', 'unique'),
	        runs = ('batsman_runs', 'sum'),
	        balls = ('ball', 'count'),     
	        date = ('date', 'unique'),
	        city = ('city', 'unique'),
	        venue = ('venue', 'unique')
	    )

		filt2 = (ball_df['batsman'] == 'RG Sharma') \
		& ((ball_df['extras_type'] == 'noballs') | ((pd.isna(ball_df['extras_type']))))

		batsmanAgainstAll = ball_df.loc[filt2]

		merge_result2 = batsmanAgainstAll.merge(match_df, how='inner', on='id')

		res2 = merge_result2.groupby(
	        ['id']
	    ).agg(
	        batman = ('batsman', 'unique'),
	        team_playing = ('batting_team', 'unique'),
	        against = ('bowling_team', 'unique'),
	        runs = ('batsman_runs', 'sum'),
	        balls = ('ball', 'count'),     
	        date = ('date', 'unique'),
	        city = ('city', 'unique'),
	        venue = ('venue', 'unique')
	    )

		# data = []
		# data.append({'ff': inputp})

		# res = json.dumps(res)

		res2 = res2.tail(15)



		return render_template('form.html', res=res.values.tolist(), res2=res2.values.tolist())

if __name__ == '__main__':
	app.run(debug=True)
