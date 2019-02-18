import boto3, decimal
import json, sys
import io_module

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')

# table name
table = dynamodb.Table('AdminDB')
brand = sys.argv[1]
products = io_module.get_json('new', brand, 'complete')
# print(products)
# Input Start
columns = ['skuid', 'name', 'url', 'image', 'color', 'category', 'salePrice', 'originalPrice', 'brand', 'volume', 'info_status', 'discon', 'request_time', 'sale_status', 'confirm_time']
for i, product in enumerate(products):
    print(product['skuid'],product['name'])
    table.put_item(Item=product)

    '''
    item = {}
    for column in columns:
        item[column] = product[column]

    print('push :', item['skuid'], item['name'])
    table.put_item(
       Item=item
    )
   '''
