
# Solution Architecture
               


The solution consists of the following components:


•	Kinesis Stream: An AWS Kinesis stream that serves as the source of events. It receives events from various sources and streams them in real-time.

•	 An SQS Queue for the incoming stream and bus system for the later processing.

•	Lambda Function: An AWS Lambda function that is triggered by events from the Kinesis stream. The Lambda function is implemented in Python 3 and processes the incoming JSON events, extracting common fields (event_uuid, event_name, created_at), adding additional fields (created_datetime, event_type, event_subtype), and storing the enriched events in an S3 bucket.

•	S3 Bucket: An AWS S3 bucket that serves as the data lake storage. The enriched events from the Lambda function are stored in the appropriate partitions in the S3 bucket based on the event_type field.


## Technologies Chosen

•	AWS Kinesis: Chosen as the event streaming service to ingest events in real-time and provide reliable and scalable data streaming capabilities.

•	AWS Lambda: Chosen as the serverless compute service to process events from the Kinesis stream in an event-driven manner without managing any servers.

• AWS SQS Scalable and Decoupled Communication to enable asynchronous communication between distributed components of an application

• AWS S3: Chosen as the data lake storage to store the enriched events in an organized and scalable manner, with built-in durability and availability.

## Design Decisions

•	Python 3: Chosen as the programming language for implementing the Lambda function due to its ease of use, extensive libraries and support for handling JSON data.

•	Boto3: Chosen as the AWS SDK for Python to interact with AWS services, including Kinesis, Lambda, and S3, due to its comprehensive coverage of AWS APIs and ease of use.

•	Partitioning in S3: Chosen as the method to organize and manage data in the S3 bucket based on the event_type field for efficient querying and retrieval of data. Partitions are created in the format "event_type=event_type_value/" to ensure data is organized in separate directories based on event types.

### Solution Deployment
## Prerequisites
•	AWS account with appropriate permissions to create and manage Kinesis streams, Lambda functions, and S3 buckets.

•	Python 3 installed on the development environment.

•	Boto3 Python library installed on the development environment.

•	Terraform installed on the development environment for provisioning AWS resources.


#### Deployment Steps
1. Clone the repository and navigate to the project directory.
2. Update the terraform.tfvars file with the appropriate values for your AWS account, region, and other configurations.
3. Run terraform init to initialize the Terraform working directory.
4. Run terraform plan to check the desired output
5. Run terraform apply to provision the AWS resources using Terraform scripts.
6. Run terrarform destroy to elimate remove all.

### Testing

#### You can use the file StreamGenerator.py for creating the 1M events
```python
$ python3 streamGenerator.py
```                                                                                                                                                       
The solution provides a scalable and event-driven approach to process and store events from a Kinesis stream in an S3 bucket. It leverages AWS Lambda for serverless compute, AWS Kinesis for real-time event streaming, and AWS S3 for data lake storage. The solution can be easily deployed and automated using Terraform, and includes tests to ensure the reliability and correctness of the implementation
