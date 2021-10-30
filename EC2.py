# This is the Flask application deployed in EC2


from flask import Flask
from flask import request
import math
import random
import json

app = Flask(__name__)

@app.route('/')
def calculate():
        incircle = 0
        in_cirList=[]
        shot_list=[]
        pi_values=[]
        shots = int(request.args.get('shots'))
        rate  = int(request.args.get('rate'))
        r_rate_values = list(range(0,shots+rate,rate))
        r_rate_values = [i for i in r_rate_values if i != 0]
        for i in range(1, shots+1):
		incircle = 0
        in_cirList=[]
        shot_list=[]
        pi_values=[]
        shots = int(request.args.get('shots'))
        rate  = int(request.args.get('rate'))
        r_rate_values = list(range(0,shots+1,rate))
        r_rate_values = [i for i in r_rate_values if i != 0]
        for i in range(1, shots+1):
                random1 = random.uniform(-1.0, 1.0)
                random2 = random.uniform(-1.0, 1.0)
                if( ( random1*random1 + random2*random2 ) < 1 ):
                        incircle += 1
                if(i in r_rate_values):
                        in_cirList.append(incircle)
                        shot_list.append(i)
        result=in_cirList,shot_list#json.dumps(in_cirList)
        result=json.dumps(result)
        return result
if __name__ == '__main__':
        app.debug = True
        app.run()


