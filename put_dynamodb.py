import boto3
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
    s3 = boto3.client('s3')  # again assumes boto.cfg setup, assume AWS S3
    compare_history = [key['Key'] for key in s3.list_objects(Bucket='cosmee-product-data')['Contents'] if key['Key'].startswith(brand + '/compare/history')]

    print(compare_history)
    for key in compare_history:
        filename = key.split('/')[-1][:-5]
        products = io_module.get_json(filename, brand, 'compare/history')
        print('--- put into AdminDB :',filename,'file ---')

        # Input Start
        for product in products:
                # print(product['skuid'],product['name'])
                table.put_item(Item=product)



if __name__ == "__main__":
    brand = sys.argv[1]
    main(brand)
