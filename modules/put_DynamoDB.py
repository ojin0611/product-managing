import boto3
import json
import decimal

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')

# table name
table = dynamodb.Table('AdminDB')
dir_name  = 'C:/Users/dongm/Downloads/'
json_name= 'old.json'

json_data=open(dir_name + json_name, encoding='UTF8').read()
products = json.loads(json_data)#, encoding='utf-8')
# Input Start
columns = ['skuid', 'name', 'url', 'image', 'color', 'category', 'salePrice', 'originalPrice', 'brand', 'volume', 'info_status', 'discon', 'request_time', 'sale_status', 'confirm_time']
for i, product in enumerate(products):
    # SKU ID function
    product['skuid']='000000000'+str(i).zfill(3) 
    # after product has 'skuid' >change> table.put_item(Item=product)

    
    item = {}
    for column in columns:
        item[column] = product[column]

    print('push :', item['skuid'], item['name'])
    table.put_item(
       Item=item
    )
