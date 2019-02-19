import boto3, decimal
import json, sys, os
sys.path.append('./modules')
import io_module

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')

# table name
table = dynamodb.Table('AdminDB')

def main(brand):
    if brand=='all':
        brandlist = next(os.walk('./crawling/'))[1]
        for brand in brandlist:
            print(brand)
            update(brand)

    else:
        update(brand)

def update(brand):
    products = io_module.get_json('new', brand, 'complete')
    # Input Start
    for i, product in enumerate(products):
        print(product['skuid'],product['name'])
        table.put_item(Item=product)



if __name__ == "__main__":
    brand = sys.argv[1]
    main(brand)
