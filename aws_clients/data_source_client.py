import boto3
from botocore.exceptions import ClientError

class DataSourceClient(object):

    @staticmethod        
    def create_data_source(client, name, knowledgeBaseId, bucket_arn, prefix):
        try:
            response = client.create_data_source(
                dataDeletionPolicy='RETAIN',
                dataSourceConfiguration={
                    's3Configuration': {
                        'bucketArn': bucket_arn,
                        'inclusionPrefixes': [
                            prefix,
                        ]
                    },
                    'type': 'S3'
                },
                knowledgeBaseId=knowledgeBaseId,
                name=name
            )
            if "dataSourceId" not in response:
                    raise Exception(f'KeyError : \'dataSourceId\' not found in response')
            if "failureReasons" in response:
                raise Exception(f'AWS Client Error : Error encountered during creation of data source : {response["failureReasons"]}')

            return response["dataSourceId"]
        
        except Exception as e:
            raise e
    
    @staticmethod
    def start_injestion_job(client, dataSourceId, knowledgeBaseId):
        try:
            response = client.start_ingestion_job(
                dataSourceId=dataSourceId,
                knowledgeBaseId=knowledgeBaseId
            )
            return response  # or process the response as needed
        except ClientError as e:
            error_message = f"An error occurred: {e.response['Error']['Message']}"
            return None  # or raise an exception or handle it accordingly
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return None  # or raise an exception or handle it accordingly
