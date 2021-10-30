#/usr/bin/env python3
import time
import http.client
import random
import project_functions
import math
import time
from math import pi
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
# creates a list of values as long as the number of things we want
# in parallel so we could associate an ID to each

pies_l=[]
def process_lamdaout(data_out):
    data_out=data_out[2:-2]
    data_out=data_out.split('"')
    
    data_out.remove(', ')
    q_rates=data_out[0][1:-1]
    incircles=data_out[1][1:-1]
    q_rates=q_rates.split(",")
    incircles=incircles.split(",")
    q_rates=[int(i) for i in q_rates]
    incircles=[int(i) for i in incircles]
    data_final=q_rates,incircles
    return data_final

def truncate(value,digits):
	digits=digits-1
	factor = 10.0 **digits
	value=math.trunc(value*factor)/factor
	return value


def sum_s(incircle,report_rate,r):
   # pies=[]
    firstsum=0
    firstshsum=0
    for i,j in enumerate(report_rate):
        firstsum=0
        for k in incircle:
            
            firstsum=firstsum+k[i]
        pies_l.append((firstsum/(j*r))*4)
    
    return pies_l[(len(pies_l)-1)],pies_l
    
    
def main(r1,d1,s1,q1):
    global parallel,runs,count,shots,r_rate,in_cirList,r_rate_values,threshold,digits,lambda_time,pi_value_right
    lambda_time=[]
    
    threshold =30
    total_lambda_calls= threshold*r1
    all_results=[]
    pi_list=[]
    retry_count=0
    pi_final=0
    df_fin=pd.DataFrame()
    run=0
    
    while(threshold>0):
        incircles=[]
        retry_count=retry_count+1
        parallel = r1
        shots=int(s1/r1)
        r_rate=q1
        digits=d1
        runs=[value for value in range(parallel)]
        count = 1000
        start = time.time()
        results = getpages()
        lambda_time.append(time.time() - start)
        
        rates=[]
        
        results=list(results)
        results_df= pd.DataFrame(results,columns=["Shots","Incircles"])
        results_df.insert(2,"Resources",[("R"+str(i+1)+" in run "+str(run)) for i in range(r1)],True)
        df_fin=df_fin.append(results_df)
        
        rates.append(results[0][0])
        for i in range(0,len(results)):
            incircles.append(results[i][1])
        
        final_pie,pies=sum_s(incircles,rates[0],r1)
        column_names=[]
        all_results=all_results+results
       
        if(truncate(final_pie,digits))==truncate(pi,digits):
            pi_final="Estimated Pi Value is",truncate(final_pie,digits)
            pi_value_right=truncate(final_pie,digits)
            break
        threshold=threshold-1
        run= run+1
        if(threshold==0):
            pi_final="Unable to find exact match for pi"
            pi_value_right=pi_final
      
    total_lambda_time= sum(lambda_time)
    print("Elapsed Time: ", total_lambda_time)

 
    lambda_duration_cost=total_lambda_time*(128/1024)*0.0000166667
    lambda_request_cost = total_lambda_calls*(0.2/1000000)
   
    total_cost = lambda_duration_cost+lambda_request_cost
    
   
    data_string=str('1')+","+str(s1)+","+str(q1)+","+str(d1)+","+str(r1)+","+str(pi_value_right)+","+str(total_cost)+","+str('lambda')
    
    results=project_functions.s3_read_write(data_string) 
    return pi_final,pies_l,df_fin,total_cost

def getpage(id):
	try:
    

	#specify api towards lambda function here
		conn= http.client.HTTPSConnection("25q1atsr6e.execute-api.us-east-1.amazonaws.com")
		user_in=str(shots)+","+str(r_rate)
		json= '{"key1":"'+user_in+'"}'
		conn.request("POST", "/default/pi_value_estimation",json)
		response = conn.getresponse()
		data_out= response.read()
		data_out= data_out.decode("utf-8")
		lambda_out=process_lamdaout(data_out)
        
	except IOError:
	        print( 'Failed to open ', host ) # Is the Lambda address correct?
	return lambda_out
	#return data,in_cirList


def getpages():
    with ThreadPoolExecutor() as executor:
        results=executor.map(getpage, runs)
    return results
if __name__ == '__main__':

    print( "Elapsed Time: ", time.time() - start)
