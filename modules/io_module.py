import json
from datetime import datetime
import sys
import os
import boto3
from botocore.errorfactory import ClientError
import pickle
from io import BytesIO
import pprint


def get_json(load_filename, brand, file_path, bucket_name = 'cosmee-product-data'):
    '''
    load_filename : 불러올 파일의 이름. 
    brand : ex) clio, drjart
    file_path : s3/brand/crawling 또는 local/brand 등 파일을 가져올 경로 설정
    
    파일을 저장할때는 new.json, old.json 중 1개만 가져온다.
    비교가 필요한경우(compare) new와 old를 각각 따로 가져온다.
    
    '''

    
    # local의 의미는 project 폴더 내에 있는 json 파일을 가져온다는 것!
    if file_path == 'local':
        file_path = './' + brand + '/'+ brand +'.json'
        with open(file_path, encoding="UTF-8") as json_data:
            print('--- load file from',file_path,'---')
            json_object = json.load(json_data)


    # crawling이 아닌 경우 모든 파일은 s3에서 가져온다.
    else:
        s3 = boto3.client('s3')
        s3_path = brand + '/' + file_path + '/'
        filename = load_filename + '.json'
        print('--- load key : s3/'+s3_path+filename+' ---')

        s3_object = s3.get_object(Bucket=bucket_name, Key=s3_path + filename)
        s3_text = s3_object['Body'].read().decode()
        json_object = json.loads(s3_text)

    return json_object


def upload_json(jsonstring, brand, file_path, bucket_name = 'cosmee-product-data'):

    '''
    jsonstring : json
    brand : ex) clio, drjart
    file_path : s3/brand/compare 또는 s3/brand/cleansing 등 파일을 업로드 할 경로 설정

    파일을 저장할때는 new.json과 history/저장날짜.json 총 2개를 저장한다.
    최초 저장 시, 빈 old.json을 생성한다.
    new.json이 기존에 있을 경우 기존 new.json으로 old.json을 덮어쓰고, 새로운 파일을 new.json에 덮어쓴다.
    '''

    # 파일 이름,경로 설정
    s3 = boto3.client('s3')
    s3_path = brand + '/' + file_path + '/'
    

    
    new_file = s3_path + 'new.json'
    old_file = s3_path + 'old.json'

    # 히스토리
    history_path = s3_path + 'history/'
    now = datetime.now()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    hour = str(now.hour)
    minute = str(now.minute)
    second = str(now.second)
    file_time = '%s-%s-%s-%s-%s-%s' % (year.zfill(4), month.zfill(2), day.zfill(2), hour.zfill(2), minute.zfill(2), second.zfill(2))
    history_file = history_path + file_time + ".json"

    output = json.dumps(jsonstring, ensure_ascii=False, indent='\t')

    print('--- save key : s3/'+new_file+' ---')
    print('--- save key : s3/'+old_file+' ---')


    # do not upload before VS not 1st time
    try:
        # check old_file doesn't exist
        s3.head_object(Bucket=bucket_name, Key=old_file) # 여기서 file이 없으면 ClientError가 발생합니다.


        print('--- old.json file is overwriten! ---')
        s3_rename = boto3.resource('s3')
        s3_rename.Object(bucket_name,old_file).delete()
        s3_rename.Object(bucket_name,old_file).copy_from(CopySource=bucket_name+'/'+new_file)
        s3_rename.Object(bucket_name,new_file).delete()

    except ClientError: # 빈 old_json 파일을 생성해줍니다.
        print('--- '+brand+' upload 1st time!')
        empty_json = [{"name": "#", "url": "#", "image": "#", "color": "#", "category": "#", "salePrice": "#", "originalPrice": "#", "brand": "#", "volume": "#", "type": "#", "skuid": "#"}]
        empty_output = json.dumps(empty_json, ensure_ascii=False, indent='\t')
        s3.put_object(Body=empty_output, Bucket=bucket_name, Key=old_file)
        
    s3.put_object(Body=output, Bucket=bucket_name, Key=new_file)
    s3.put_object(Body=output, Bucket=bucket_name, Key=history_file)



def get_sku_json(file_name, brand):
    '''
    skuid별로 상품을 저장해놓은 json파일을 가져온다!

    문제점 : cleansing 후에 sku_json 업데이트되는데, 
    크롤링오류때문에 백업본으로 돌아가고싶을 때 
    sku_json 파일은 특정 시간부터 쌓인 부분을 선택하여 삭제하기가 힘들다.

    개선법 : sku_json을 별도로 저장하지 않는 방법을 고안한다.
    
    '''

    s3 = boto3.client('s3')
    bucket_name = 'cosmee-product-data'
    s3_path = brand + '/' + "sku_dict" + '/'


    try:
        s3_object = s3.get_object(Bucket=bucket_name, Key=s3_path + file_name)
        s3_text = s3_object['Body'].read().decode()
        result = json.loads(s3_text)

    # 기존에 sku_json 파일이 없을 경우에는 빈 object를 return합니다.
    except ClientError:
        result = [{"brand": "#", "name": "#", "color": "#","volume": "#", "type": "#",
                   "name_id": "000000", "cvt_id": "000"}]
    print('--- load key : s3/' + s3_path + file_name + ' ---')
    return result




def upload_sku_json(data, file_name, brand):
    '''
    sku_naming 부여 후, s3에 저장
    '''

    s3 = boto3.client('s3')
    bucket_name = 'cosmee-product-data'
    s3_path = brand + '/' + "sku_dict" + '/'
    output = json.dumps(data, ensure_ascii=False, indent='\t')
    s3.put_object(Body=output, Bucket=bucket_name, Key=s3_path + file_name)
    print('--- upload key : s3/' + s3_path + file_name + ' ---')

