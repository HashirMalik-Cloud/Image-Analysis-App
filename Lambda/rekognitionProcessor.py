import json
import boto3

rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("EVENT:", json.dumps(event))  

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        },
        MaxLabels=10
    )
    
    # Only pick labels with confidence ≥ 90
    labels = [label['Name'] for label in response['Labels'] if label['Confidence'] >= 90]

    # Save simplified result
    result = {
        'Detected_Labels': labels
    }

    output_key = key.rsplit('.', 1)[0] + '_result.json'
    s3.put_object(
        Bucket='<Results Bucket Name',  
        Key=output_key,
        Body=json.dumps(result),
        ContentType='application/json'
    )

    print("Labels Saved:", labels)  
