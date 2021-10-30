# This is the main function which used Monte Carlo Method Created in AWS_Lambda


import json
import random 

def lambda_handler(event, context):
  
    incircle = 0
    in_cirList=[]
    shot_list=[]
    pi_values=[]
    user_input = (event['key1'])
    
    user_input=user_input.split(",")
    
    shots = int(user_input[0])
    rate  = int(user_input[1])
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
   


    return str(r_rate_values),str(in_cirList)
    

