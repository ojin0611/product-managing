import boto3
import sys
import json

# Create an S3 client
s3 = boto3.client('s3')

# directory + filename 을 넣고 filename으로 저장
brand = sys.argv[1]
local_path  = '../data/'+brand+'/compare/'
s3_path = brand + '/compare/'
filename = 'new.json'
bucket_name = 'cosmee-product-data'

# Uploads the given file using a managed uploader, which will split up large
# files automatically and upload parts in parallel.
'''
s3.upload_file(local_path + filename, bucket_name, s3_path + filename)
print('Upload Complete! - ',filename)
'''

s3 = boto3.client('s3')
s3_object = s3.get_object(Bucket=bucket_name, Key=s3_path + filename)
s3_text = s3_object['Body'].read().decode()
json_product = json.loads(s3_text)
for jsonfile in json_product:
    print(jsonfile.keys())
    break

# Method 2: Client.put_object()
client = boto3.client('s3')
client.put_object(Body=s3_text, Bucket=bucket_name, Key=s3_path + 'test.txt')