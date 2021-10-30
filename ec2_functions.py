#/usr/bin/env python3
import time
import http.client
import random
import math
import project_functions
from math import pi
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import requests
import json

pies_l=[]

def sum_s(incircle,report_rate,r):
   
    firstsum=0
    firstshsum=0
    for i,j in enumerate(report_rate):
        firstsum=0
        for k in incircle:
            firstsum=firstsum+k[i]
        pies_l.append((firstsum/(j*r))*4)
    return pies_l[(len(pies_l)-1)],pies_l

def truncate(value,digits):
	digits=digits-1
	factor = 10.0 **digits
	value=math.trunc(value*factor)/factor
	return value  
    
def ec2_estimation(r1,d1,s1,q1):
    global parallel,runs,count,shots,r_rate,in_cirList,r_rate_values,threshold,digits,ip_list
    threshold =30
    all_results=[]
    pi_list=[]
    retry_count=0
    pi_final=0
    df_fin=pd.DataFrame()
    run=0
    parallel = r1
    shots=int(s1/r1)
    r_rate=q1
    digits=d1
    shots=int(s1/r1)
    ip_list=project_functions.create_ec2instances(r1)
    ec2_start_time= time.time()
    q_string='/?shots={}&rate={}'.format(shots,r_rate)
    for i in range(0,len(ip_list)):
    	ip_list[i]='http://'+ip_list[i]+q_string
    while(threshold>0):
        incircles=[]
        retry_count=retry_count+1
        runs=[value for value in range(parallel)]
        count = 1000
        start = time.time()
        results = getpages()
        rates=[]
        
        results=list(results)
        results_df= pd.DataFrame(results,columns=["Shots","Incircles"])
        results_df.insert(2,"Resources",[("R"+str(i+1)+" in run "+str(run)) for i in range(r1)],True)
        df_fin=df_fin.append(results_df)
        rates.append(results[0][1])
        incircles=[results[i][0] for i in range(0,parallel)]
        final_pie,pies=sum_s(incircles,rates[0],r1)
        column_names=[]
        all_results=all_results+results
       
        if(truncate(final_pie,digits))==truncate(pi,digits):
            pi_final="Estimated Pi Value is",truncate(final_pie,digits)
            print("success")
            break
        threshold=threshold-1
        run= run+1
        if(threshold==0):
            pi_final="Unable to find exact match for pi"
    data_string=str('1')+","+str(s1)+","+str(q1)+","+str(d1)+","+str(r1)+","+str(pi_final)+","+str('0.1027')+","+str('ec2')
    project_functions.s3_read_write(data_string)   
    # Terminate all instances that are running
    #project_functions.terminate_ec2()
    ec2_end_time= time.time()
    ec2_time=(ec2_end_time - ec2_start_time)*r1
    print("Elapsed Time: ",ec2_time)
    ec2_time_hrs=ec2_time/(60*60)
    total_cost=ec2_time_hrs*0.0116
    return pi_final,pies_l,df_fin,total_cost

def getpage(id):
	dns=ip_list[id]
	print(dns)
	
	
	out=requests.get(dns,verify=False)
	out_d=out.text
	out_fin=json.loads(out_d)
	return out_fin
   



def getpages():
    with ThreadPoolExecutor() as executor:
        results=list(executor.map(getpage, runs))
    return results
if __name__ == '__main__':
    

    print( "Elapsed Time: ", time.time() - start)
