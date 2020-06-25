import os
import json
import pandas as pd
import numpy as np
from flask import Flask, jsonify, request, render_template
from tensorflow.compat.v1.keras.models import load_model

model_file_name = os.path.join("assets/models/sac_model", 'sac_ppg_model.h5')

app = Flask(__name__)
kings_model = load_model(model_file_name)
lakers_model = load_model("assets/models/lal_model/lal_ppg_model.h5")
warriors_model = load_model("assets/models/gsw_model/gsw_ppg_model.h5")

@app.route("/")
def index(): 
	return render_template('index.html')

@app.route("/analyze/<team>")
def analyze(team):
	return render_template('analyze.html', team_name=team)

@app.route('/result',methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
		result = request.form.to_dict()
		if result['team']== 'kings':
			model = kings_model
		elif result['team'] == 'lakers':
			model = lakers_model
		elif result['team'] == 'warriors':
			model = warriors_model

		result['fg%'] = int(result['fg%']) / 100
		result['ft%'] = int(result['ft%']) / 100
		result['3p%'] = int(result['3p%']) / 100
		result['vs_fg%'] = int(result['vs_fg%']) / 100
		result['vs_ft%'] = int(result['vs_ft%']) / 100
		result['vs_3p%'] = int(result['vs_3p%']) / 100

	df = pd.DataFrame(result, index=[0])
	df = df[['is_home', 'W', 'ast', 'reb', 'fg%', 'ft%', '3p%', 'vs_pts', 'vs_ast', 'vs_reb', 'vs_fg%', 'vs_ft%', 'vs_3p%']]
	df_array = np.array(df, dtype=np.float)
	predicted_ppg = model.predict(df_array)
	result['predicted_ppg'] = str(int(round(predicted_ppg[0][0])))

	return render_template('result.html', result=result)

if __name__ == '__main__':
	app.run(debug = True)
