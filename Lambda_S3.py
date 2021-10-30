# This is the Lambda code for reading and writing data to Amazon S3

import boto3
import json

region = "us-east-1"

instances = 'i-0b093a0e74178f892'

ec2 = boto3.client("ec2", region_name=region)

def checking():
    response = ec2.describe_instance_status(InstanceIds=[instances])
    if len(response["InstanceStatuses"])==0:
        print(response)
        checking()
    return

def lambda_handler(event, context):
    
    button=int(event['key1'])
    if button==1:
        ec2.start_instances(InstanceIds=[instances])
        
        checking()
        
        
        status="Instance is getting started: " + str(instances)
        #call some delay function
    elif button==2:
        ec2.stop_instances(InstanceIds=[instances])
        status="Instance have stopped: " + str(instances)
    elif button==3:
        ec22=boto3.resource("ec2",region_name=region)
        instances=ec22.create_instances (ImageId='ami-0d967e074c3a82453', MinCount=1,
        MaxCount=3,InstanceType='t2.micro', KeyName='us-east-1kp')
        #checking()
        instance=instances[0]
        instance.wait_until_running()
        instance.load()
        publcdns=instance.public_dns_name
        #status="Instance have stopped: " + str(instances)
 
    return publcdns
