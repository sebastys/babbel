import datetime
import json
import boto3

# Create a Kinesis client
kinesis_client = boto3.client('kinesis', region_name='eu-north-1')  # Replace with your desired region

# Create a Kinesis stream
stream_name = 'my-kinesis-stream'  # Replace with your desired stream name
shard_count = 1  # Number of shards in the stream
kinesis_client.create_stream(StreamName=stream_name, ShardCount=shard_count)

# Wait for the stream to become active
kinesis_client.get_waiter('stream_exists').wait(StreamName=stream_name)

# Put a sample event to the stream
sample_event = {
    'event_uuid': '12345',
    'event_name': 'example:event_type:event_subtype',
    'created_at': 1672531199,  # Replace with your desired Unix timestamp
    'payload_field1': 'value1',  # Replace with your event payload fields
    'payload_field2': 'value2',
}

# Add additional fields to the event
sample_event['created_datetime'] = datetime.datetime.fromtimestamp(sample_event['created_at']).isoformat()
event_name_parts = sample_event['event_name'].split(':')
sample_event['event_type'] = event_name_parts[0]
sample_event['event_subtype'] = event_name_parts[1]

# Put the event to the Kinesis stream
kinesis_client.put_record(StreamName=stream_name, Data=json.dumps(sample_event), PartitionKey='event_uuid')
