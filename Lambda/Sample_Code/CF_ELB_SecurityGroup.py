
event = {
  "Records": [
    {
      "EventVersion": "1.0",
      "EventSubscriptionArn": "arn:aws:sns:EXAMPLE",
      "EventSource": "aws:sns",
      "Sns": {
        "SignatureVersion": "1",
        "Timestamp": "1970-01-01T00:00:00.000Z",
        "Signature": "EXAMPLE",
        "SigningCertUrl": "EXAMPLE",
        "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
        "Message": "{\"create-time\": \"yyyy-mm-ddThh:mm:ss+00:00\", \"synctoken\": \"0123456789\", \"md5\": \"4f1af31d53ea099646367215dcda798d\", \"url\": \"https://ip-ranges.amazonaws.com/ip-ranges.json\"}",
        "Type": "Notification",
        "UnsubscribeUrl": "EXAMPLE",
        "TopicArn": "arn:aws:sns:EXAMPLE",
        "Subject": "TestInvoke"
      }
    }
  ]
}

import boto3
import hashlib
import json
import urllib.request

SERVICE = "CLOUDFRONT"
INGRESS_PORTS = { 'Http' : 80, 'Https': 443 }
CF_TYPE = "GLOBAL"        # "GLOBAL" | "REGION"
CF_PORT = 80
# Tags which identify the security groups you want to update
SECURITY_GROUP_TAG_FOR_GLOBAL_HTTP1 = { 'Name': 'teamkorea-alb-sg' }
SECURITY_GROUP_TAG_FOR_GLOBAL_HTTP2 = { 'Name': 'teamkorea-alb-second-sg' }

def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    ip_ranges = json.loads(get_ip_groups_json(message['url'], message['md5']))
        
    if CF_TYPE == 'GLOBAL':
      cf_ranges = get_ranges_for_service(ip_ranges, SERVICE, "GLOBAL")
    elif CF_TYPE == 'REGION':
      cf_ranges = get_ranges_for_service(ip_ranges, SERVICE, "REGION")


    add_security_group_rules(cf_ranges)
    return ip_ranges

def get_ip_groups_json(url, expected_hash):
    response = urllib.request.urlopen(url)
    ip_json = response.read()

    m = hashlib.md5()
    m.update(ip_json)
    hash = m.hexdigest()

    if hash != expected_hash:
        raise Exception('MD5 Mismatch: got ' + hash + ' expected ' + expected_hash)

    return ip_json

def get_ranges_for_service(ranges, service, subset):
    service_ranges = list()
    for prefix in ranges['prefixes']:
        if prefix['service'] == service and ((subset == prefix['region'] and subset == "GLOBAL") or (subset != 'GLOBAL' and prefix['region'] != 'GLOBAL')):
            service_ranges.append(prefix['ip_prefix'])

    return service_ranges

def add_security_group_rules(cidr_blocks, security_group_name1=SECURITY_GROUP_TAG_FOR_GLOBAL_HTTP1['Name'], security_group_name2=SECURITY_GROUP_TAG_FOR_GLOBAL_HTTP2['Name']):
    ec2_client = boto3.client('ec2')
    response1 = ec2_client.describe_security_groups(Filters=[{'Name': 'tag:Name', 'Values': [security_group_name1]}])
    response2 = ec2_client.describe_security_groups(Filters=[{'Name': 'tag:Name', 'Values': [security_group_name2]}])
    security_group_id1 = response1['SecurityGroups'][0]['GroupId']
    security_group_id2 = response2['SecurityGroups'][0]['GroupId']

    for cidr_block in cidr_blocks[:60]:
        # Check if the rule already exists in security_group_id1
        existing_rules = response1['SecurityGroups'][0]['IpPermissions']
        if check_rule_exists(existing_rules, cidr_block):
            print(f"Rule for {cidr_block} already exists in {security_group_name1}. Skipping...")
            continue

        ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id1,
            IpProtocol='tcp',
            FromPort=CF_PORT,
            ToPort=CF_PORT,
            CidrIp=cidr_block
        )

    for cidr_block in cidr_blocks[60:]:
        # Check if the rule already exists in security_group_id2
        existing_rules = response2['SecurityGroups'][0]['IpPermissions']
        if check_rule_exists(existing_rules, cidr_block):
            print(f"Rule for {cidr_block} already exists in {security_group_name2}. Skipping...")
            continue
        else:
            print(f"Rule for {cidr_block} is created in {security_group_name2}....")


        ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id2,
            IpProtocol='tcp',
            FromPort=CF_PORT,
            ToPort=CF_PORT,
            CidrIp=cidr_block
        )


def check_rule_exists(existing_rules, cidr_block):
    for rule in existing_rules:
        if 'IpRanges' in rule:
            for ip_range in rule['IpRanges']:
                if ip_range['CidrIp'] == cidr_block:
                    return True
    return False
