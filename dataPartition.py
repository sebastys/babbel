import boto3

# Define your S3 bucket name
BUCKET_NAME = 'my-s3-bucket' 

# Define the event types for which partitions need to be created
EVENT_TYPES = ['event_type1', 'event_type2', 'event_type3'] 

def create_s3_partition(bucket_name, partition_key, partition_value):
    """
    Create a partition in an S3 bucket based on the given partition key and value.
    """
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    # Format the partition path in the format "partition_key=partition_value/"
    partition_path = f'{partition_key}={partition_value}/'
    # Create an empty object in the partition to create the partition
    bucket.put_object(Key=partition_path)

if __name__ == '__main__':
    # Loop through each event type and create a partition in S3 bucket
    for event_type in EVENT_TYPES:
        create_s3_partition(BUCKET_NAME, 'event_type', event_type)
        print(f'S3 partition created for event type: {event_type}')
