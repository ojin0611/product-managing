import json
from datetime import datetime
import sys
import os
import boto3
from botocore.errorfactory import ClientError


def get_json(load_filename, brand, activity):
    # load_filename : new / old
    # brand : name of brand
    # activity : crawling / cleansing / compare

    if activity == 'local':     # crawling
        file_path = './' + brand + '/'+ brand +'.json'
        with open(file_path, encoding="UTF-8") as json_data:
            print('--- load file from',file_path,'---')
            json_object = json.load(json_data)

    else:
        s3 = boto3.client('s3')
        bucket_name = 'cosmee-product-data'
        s3_path = brand + '/' + activity + '/'
        filename = load_filename + '.json'
        print('--- load key : s3/'+s3_path+filename+' ---')

        s3_object = s3.get_object(Bucket=bucket_name, Key=s3_path + filename)
        s3_text = s3_object['Body'].read().decode()
        json_object = json.loads(s3_text)
    
    return json_object

def upload_json(jsonstring, brand, activity):

    # jsonstring : json
    # brand : name of brand
    # activity : crawling / cleansing / compare
    s3 = boto3.client('s3')
    bucket_name = 'cosmee-product-data'
    s3_path = brand + '/' + activity + '/'
    
    new_file = s3_path + 'new.json'
    old_file = s3_path + 'old.json'

    history_path = s3_path + 'history/'
    now = datetime.now()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    hour = str(now.hour)
    minute = str(now.minute)
    second = str(now.second)
    file_time = '%s-%s-%s-%s-%s-%s' % (year.zfill(4), month.zfill(2), day.zfill(2),
                                       hour.zfill(2), minute.zfill(2), second.zfill(2))
    history_file = history_path + file_time + ".json"

    output = json.dumps(jsonstring, ensure_ascii=False, indent='\t')

    print('--- save key : s3/'+new_file+' ---')
    print('--- save key : s3/'+old_file+' ---')


    # crawling first vs crawling again
    try:
        # check if crawled before (== old file doesn't exist)
        s3.head_object(Bucket=bucket_name, Key=old_file)
        print('--- old.json file is overwriten! ---')
        s3_rename = boto3.resource('s3')
        s3_rename.Object(bucket_name,old_file).delete()
        s3_rename.Object(bucket_name,old_file).copy_from(CopySource=bucket_name+'/'+new_file)
        s3_rename.Object(bucket_name,new_file).delete()
    except ClientError: # crawling 1st time!
        print('--- '+brand+' upload 1st time!')
        empty_json = [{"name": "#", "url": "#", "image": "#", "color": "#", "category": "#", "salePrice": "#",
                       "originalPrice": "#", "brand": "#", "volume": "#", "type": "#", "skuid": "#"}]
        empty_output = json.dumps(empty_json, ensure_ascii=False, indent='\t')
        s3.put_object(Body=empty_output, Bucket=bucket_name, Key=old_file)
        
    s3.put_object(Body=output, Bucket=bucket_name, Key=new_file)
    s3.put_object(Body=output, Bucket=bucket_name, Key=history_file)