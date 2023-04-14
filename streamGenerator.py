import boto3
import datetime
import json

#A simple Python Script for generating a numer of events to a Kinesis Data Stream

# Create a Kinesis client
kinesis_client = boto3.client('kinesis', region_name='eu-norht-1')  # Replace with your desired region

# Create a Kinesis stream
stream_name = 'babbel-kinesis-stream'  # Replace with your desired stream name
shard_count = 1  # Number of shards in the stream
kinesis_client.create_stream(StreamName=stream_name, ShardCount=shard_count)

# Wait for the stream to become active
kinesis_client.get_waiter('stream_exists').wait(StreamName=stream_name)

# Put events to the stream
events = []  # List to store events
for i in range(1000000):  # Generating 1 million events
    # Generate sample event
    event_uuid = f'event_{i}'
    event_name = f'example:event_type{i % 10}:event_subtype{i % 5}'
    created_at = int(datetime.datetime.now().timestamp())
    payload_field1 = f'value1_{i}'
    payload_field2 = f'value2_{i}'

    # Create event dictionary
    event = {
        'event_uuid': event_uuid,
        'event_name': event_name,
        'created_at': created_at,
        'payload_field1': payload_field1,
        'payload_field2': payload_field2,
    }

    # Add additional fields to the event
    event['created_datetime'] = datetime.datetime.fromtimestamp(created_at).isoformat()
    event_name_parts = event_name.split(':')
    event['event_type'] = event_name_parts[0]
    event['event_subtype'] = event_name_parts[1]

    events.append(event)

    # Put the event to the Kinesis stream
    kinesis_client.put_record(StreamName=stream_name, Data=json.dumps(event), PartitionKey=event_uuid)

print(f'Successfully put {len(events)} events to the Kinesis stream.')
