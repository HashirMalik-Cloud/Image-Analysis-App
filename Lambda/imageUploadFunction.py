import json
import boto3
import os
import uuid

s3 = boto3.client('s3')
BUCKET = os.environ['UPLOAD_BUCKET']

def lambda_handler(event, context):
    method = event.get('requestContext', {}).get('http', {}).get('method', 'GET')

    if method == "OPTIONS":
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,GET,PUT',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': ''
        }

    try:
        # Generate UUID for file
        unique_id = str(uuid.uuid4())

        # File paths
        image_key = f"Analysis/{unique_id}.jpg"
        result_key = f"Analysis/{unique_id}_result.json"

        # Generate presigned URL for uploading the image
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={'Bucket': BUCKET, 'Key': image_key, 'ContentType': 'image/jpeg'},
            ExpiresIn=300
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'uploadURL': presigned_url,
                'filename': image_key,
                'resultFilename': result_key
            }),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,GET,PUT',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Content-Type': 'application/json'
            }
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,GET,PUT',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Content-Type': 'application/json'
            }
        }
