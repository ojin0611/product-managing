import boto3, decimal
import json, sys
import io_module

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')

# table name
table = dynamodb.Table('AdminDB')
brand = sys.argv[1]
products = io_module.get_json('new', brand, 'complete')

# Input Start
for i, product in enumerate(products):
    print(product['skuid'],product['name'])
    table.put_item(Item=product)

