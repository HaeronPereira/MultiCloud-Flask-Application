import os
import pandas as pd
import numpy as np
import http.client
import requests
import time
import queue
import threading
import boto3
import json
import time

from concurrent.futures import ThreadPoolExecutor


def ec2_start_stop(s):
	

	c = http.client.HTTPSConnection("ydryrze2ki.execute-api.us-east-1.amazonaws.com") #amazon lambda api
	s=str(s)
	json= '{ "key1":"'+s+'"}'
	c.request("POST", "/default/ec2_start_stop", json)
	response = c.getresponse()
	data2 = response.read()
	data2=data2.decode("utf-8")
	return data2
	
def s3_read_write(data_string):
	print("inside read write s3")
	c = http.client.HTTPSConnection("x2q8k4hdfh.execute-api.us-east-1.amazonaws.com") #amazon lambda api 
	json= '{ "key1":"'+data_string+'"}'
	c.request("POST", "/default/s3_historystorage", json)
	response = c.getresponse()
	data_out = response.read()
	data_out=data_out.decode("utf-8")
	return data_out

def get_instance_ip(instances):
	iplist=[]
	for instance in instances:
		instance.wait_until_running()
		instance.load()
		publcip=instance.public_ip_address
		iplist.append(publcip)
	return iplist

	
def create_ec2instances(r):
	os.environ['AWS_SHARED_CREDENTIALS_FILE']='./cred'
	# Above line needs to be here before boto3 to ensure file is read
	import boto3
	region = "us-east-1"
	ec2 = boto3.resource('ec2',region_name=region)
	instances=ec2.create_instances(ImageId='ami-0b13bf0b24056fa10',
	MinCount=1,
	MaxCount=r,
	InstanceType='t2.micro',
	KeyName='us-east-1kp',SecurityGroupIds=['SSH_CourseWork'])

	ip_list=get_instance_ip(instances)

	return(ip_list)
def terminate_ec2():
	os.environ['AWS_SHARED_CREDENTIALS_FILE']='./cred'	
	import boto3
	region = "us-east-1"
	ec2 = boto3.resource('ec2',region_name=region)
	instances=ec2.instances.all()
	instancelist=[]
	for instance in instances:
		if(instance.state['Name']=='running'):
			instancelist.append(instance.id)

	ec2.instances.filter(InstanceIds = instancelist).terminate()	
	return(instancelist)


