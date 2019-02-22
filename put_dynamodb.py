import boto3
import json, sys, os, re
sys.path.append('./modules')
import io_module

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')

# table name
table = dynamodb.Table('AdminDB')

def getUpdateTime(string):
    numExtracter = re.compile('[0-9]+')
    return int(''.join(numExtracter.findall(string)))

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
    try:
        admindb_history = [key['Key'] for key in s3.list_objects(Bucket='cosmee-admindb')['Contents'] if key['Key'].startswith('AdminDB/backup/history')]
    except KeyError:
        print('--- AdminDB backup file not exists ---')
        return

    last_backup_time = admindb_history[-1].split('/')[-1][:-5]
    print('--- Last Backup Time :',last_backup_time)
    last_backup_time = getUpdateTime(last_backup_time)

    for key in compare_history:
        filename = key.split('/')[-1][:-5]
        if getUpdateTime(filename) > last_backup_time:
            products = io_module.get_json(filename, brand, 'compare/history')
            print('--- put AdminDB:',brand,filename,'file ---')

            # Input Start
            for product in products:
                try:
                    # print(product['skuid'],product['name'])
                    table.put_item(Item=product)
                except:
                    pass
        else:
            pass


if __name__ == "__main__":
    brand = sys.argv[1]
    main(brand)
