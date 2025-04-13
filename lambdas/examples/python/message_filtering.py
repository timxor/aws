import json
import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Define keywords to filter messages
    keywords = ['urgent', 'important', 'alert']
    
    # Parse incoming webhook payload
    try:
        body = json.loads(event.get('body', '{}'))
        messages = body.get('messages', [])
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON payload'})
        }
    
    # Filter messages based on keywords in subject
    filtered_messages = []
    for message in messages:
        subject = message.get('subject', '').lower()
        if any(keyword.lower() in subject for keyword in keywords):
            filtered_messages.append({
                'subject': message.get('subject'),
                'body': message.get('body')
            })
    
    # If no messages match, return early
    if not filtered_messages:
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'No matching messages found'})
        }
    
    # Store filtered messages in S3
    try:
        bucket_name = 'webhook-bucket'
        key = f'filtered_messages_{context.aws_request_id}.json'
        s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=json.dumps(filtered_messages, indent=2),
            ContentType='application/json'
        )
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Failed to store in S3: {str(e)}'})
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'Successfully processed {len(filtered_messages)} messages',
            'stored_at': f's3://{bucket_name}/{key}'
        })
    }

