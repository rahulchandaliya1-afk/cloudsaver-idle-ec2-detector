import boto3
from datetime import datetime, timedelta

# Create clients with region
ec2 = boto3.client('ec2', region_name='us-east-1')
cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

def find_idle_instances():
    instances = ec2.describe_instances()
    idle = []

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']

            metrics = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                StartTime=datetime.utcnow() - timedelta(hours=1),
                EndTime=datetime.utcnow(),
                Period=300,
                Statistics=['Average']
            )

            if metrics['Datapoints']:
                avg_cpu = metrics['Datapoints'][0]['Average']
                if avg_cpu < 5:
                    idle.append(instance_id)

    return idle

print("Idle instances:", find_idle_instances())
