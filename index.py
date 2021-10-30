import os
import logging
import http.client
import json
import requests
import ast
import queue
import threading
import multiprocessing
import time
import pandas as pd

from math import pi
import parallel
import ec2_functions
import project_functions
from IPython.display import HTML



from flask import Flask, request, render_template,redirect

app = Flask(__name__)

# various Flask explanations available at: https://flask.palletsprojects.com/en/1.1.x/quickstart/

	
def doRender(tname, values={}):
	
	if not os.path.isfile( os.path.join(os.getcwd(), 'templates/'+tname) ): #No such file
		return render_template('index.htm')
	return render_template(tname, **values)


# Defines a POST supporting calculate route
@app.route('/calculate', methods=['GET','POST'])
def calculateHandler():
	#if request.method == 'POST':
	R = int(request.form.get('resources'))
	S = int(request.form.get('shots'))
	Q = int(request.form.get('rate'))
	D = int(request.form.get('digits'))
	service=request.form['service']
	print("...................................",service)
	if service == 'lambda':
		final_pi,pi_list,df_fin,run_cost  = parallel.main(R,D,S,Q)
		x_axis=[i for i in range(len(pi_list))]
		pi_org = [round(pi,D)]*len(pi_list)
		df_fin.reset_index(drop=True, inplace=True)
		#table=[df_fin.to_html(classes='data',escape=False)]
	if service == 'ec2':
		final_pi,pi_list,df_fin,run_cost  = ec2_functions.ec2_estimation(R,D,S,Q)
		x_axis=[i for i in range(len(pi_list))]
		pi_org = [round(pi,D)]*len(pi_list)
		df_fin.reset_index(drop=True, inplace=True)
		
	return render_template('page2.htm', data=final_pi,data2=pi_list,x_axis=x_axis,fixed_pie=pi_org,rate=Q,resource=R,shots=S,digits=D,df=[df_fin.to_html(classes='data',escape=False)],titles=df_fin.columns.values,cost=run_cost,service = service)


@app.route('/history', methods=['GET','POST'])
def pi_history():
	
	results=project_functions.s3_read_write(str(2)) # call lambda function to get data from s3 bucket
	json_out=json.loads(results)
	hist_df=pd.DataFrame()
	for i in range(0,len(json_out)):
		data_json=json.loads(json_out[i])
		json_df=pd.DataFrame(list(data_json.values()))
		json_df=json_df.T
		json_df.columns=['Shots','Reporting Rate','Digits','Resources','Pi_value_estimated','Cost','Service']
		hist_df=hist_df.append(json_df)
	hist_df.reset_index(drop=True, inplace=True)
	hist_df_html=[hist_df.to_html(classes='data',escape=False)]
	return render_template('history.htm',table=hist_df_html,titles=hist_df.columns.values)

@app.route('/terminate', methods=['GET','POST'])
def Terminate():
	project_functions.terminate_ec2()
	return doRender('terminate.htm')
	
#******************************************************************************************************************************************

@app.route('/', defaults={'path': ''})

@app.route('/<path:path>')

def mainPage(path):

   return doRender(path)


@app.errorhandler(500)



def server_error(e):

   #logging.exception('ERROR!')

   return """
An error occurred: <pre>{}</pre>
""".format(e), 500


if __name__ == '__main__':
	print(logging.__file__)
	app.run(host='127.0.0.1',port=8081,debug=True)
# catch all other page requests - doRender checks if a page is available (shows it) or not (index)


