import boto3
import json, sys
sys.path.append('./modules')
import io_module


def main():
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')

    # table name
    table = dynamodb.Table('AdminDB')

    response = table.scan(
        Select="ALL_ATTRIBUTES",
        )

    json_list = []
    for item in response['Items']:
        json_list.append(item)

    io_module.upload_json(json_list, 'AdminDB', 'backup', bucket_name = 'cosmee-admindb')


if __name__ == "__main__":
    main()
