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


@app.route('/batsmanAgainstteam', methods=['GET', 'POST'])
def batsmanAgainstteam():
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
        batman=('batsman', 'unique'),
        team_playing=('batting_team', 'unique'),
        against=('bowling_team', 'unique'),
        runs=('batsman_runs', 'sum'),
        balls=('ball', 'count'),
        date=('date', 'unique'),
        city=('city', 'unique'),
        venue=('venue', 'unique')
    )

	filt2 = (ball_df['batsman'] == inputPlayer) \
	& ((ball_df['extras_type'] == 'noballs') | ((pd.isna(ball_df['extras_type']))))

	batsmanAgainstAll = ball_df.loc[filt2]

	merge_result2 = batsmanAgainstAll.merge(match_df, how='inner', on='id')

	res2 = merge_result2.groupby(
        ['id']
    ).agg(
        batman=('batsman', 'unique'),
        team_playing=('batting_team', 'unique'),
        against=('bowling_team', 'unique'),
        runs=('batsman_runs', 'sum'),
        balls=('ball', 'count'),
        date=('date', 'unique'),
        city=('city', 'unique'),
        venue=('venue', 'unique')
    )

	# data = []
	# data.append({'ff': inputp})

	# res = json.dumps(res)

	return render_template('batsmanAgainstteam.html', res=res.values.tolist(), res2=res2.values.tolist(), inputPlayer=inputPlayer)


@app.route('/bowlerAgainstteam', methods=['GET', 'POST'])
def bowlerAgainstteam():
	inputPlayer = request.form.get("playerName")
	inputTeam = request.form.get("AgainstTeam")

	ball_df = pd.read_csv('data/IPL Ball-by-Ball 2008-2020.csv')
	match_df = pd.read_csv('data/IPL Matches 2008-2020.csv')

	filt = (ball_df['bowler'] == inputPlayer) & \
    (ball_df['batting_team'] == inputTeam)
	bowlerAgainstTeam = ball_df.loc[filt]

	merge_result = bowlerAgainstTeam.merge(match_df, how='inner', on='id')

	res = merge_result.groupby(
        ['id']
    ).agg(
        bowler=('bowler', 'unique'),
        team_playing=('bowling_team', 'unique'),
        against=('batting_team', 'unique'),
        runs=('total_runs', 'sum'),
        balls=('ball', 'count'),
        wickets=('is_wicket', 'sum'),
        date=('date', 'unique'),
        city=('city', 'unique'),
        venue=('venue', 'unique')
    )

	filt2 = (ball_df['bowler'] == inputPlayer)

	bowlerAgainstTeam = ball_df.loc[filt2]

	merge_result = bowlerAgainstTeam.merge(match_df, how='inner', on='id')

	res2 = merge_result.groupby(
        ['id']
    ).agg(
        bowler = ('bowler', 'unique'),
        team_playing = ('bowling_team', 'unique'),
        against = ('batting_team', 'unique'),
        runs = ('total_runs', 'sum'),
        balls = ('ball', 'count'),    
        wickets = ('is_wicket', 'sum'),
        date = ('date', 'unique'),
        city = ('city', 'unique'),
        venue = ('venue', 'unique')
    )

	res2 = res2.tail(20)
   
	return render_template('bowlerAgainstteam.html', res=res.values.tolist(), res2=res2.values.tolist(), inputPlayer=inputPlayer)

@app.route('/pitch', methods=['GET', 'POST'])
def pitch():

	return render_template('pitch.html')

if __name__ == '__main__':
	app.run(debug=True)
