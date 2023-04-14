import json
import boto3
from datetime import datetime

# Create S3 client
s3_client = boto3.client('s3')

# Lambda handler function
def lambda_handler(event, context):
    try:
        # Iterate through Kinesis stream records
        for record in event['Records']:
            # Extract the event data from the record
            event_data = json.loads(record['kinesis']['data'])
            
            # Extract common fields from the event data
            event_uuid = event_data['event_uuid']
            event_name = event_data['event_name']
            created_at = event_data['created_at']
            
            # Enrich the event data with additional fields
            created_datetime = datetime.utcnow().isoformat() 
            event_type = 'enriched'  
            event_subtype = 'new'  
            
            # Add the enriched fields to the event data
            event_data['created_datetime'] = created_datetime
            event_data['event_type'] = event_type
            event_data['event_subtype'] = event_subtype
            
            # Convert the event data back to JSON
            enriched_event_data = json.dumps(event_data)
            
            # Store the enriched event data in S3 bucket
            s3_client.put_object(
                Body=enriched_event_data,
                Bucket='example-s3-bucket', 
                Key=f'{event_type}/{event_uuid}.json' # S3 object key
            )
            
    except Exception as e:
        print(f'Error processing Kinesis stream event: {e}')
        raise e

    return {
        'statusCode': 200,
        'body': 'Successfully processed Kinesis stream event'
    }
