import boto3
from utils.helpers import generate_unique_name
from aws_clients.knowledge_base_client import KnowledgeBaseClient
from aws_clients.data_source_client import DataSourceClient
from aws_clients.s3_client import S3Client

class BedRockAgent(object):
    def __init__(self) -> None:
        self.client = boto3.client('bedrock-agent')
        
    def create_knowledge_base(self, title=None, uploaded_files=None):
        # create knowledge base 
        name = generate_unique_name(resource_name='knowledge-base', title=title)
        role_arn = 'arn:aws:iam::054244991161:role/service-role/AmazonBedrockExecutionRoleForKnowledgeBase_pokji'
        name, knowledgeBaseId, knowledgeBaseArn = KnowledgeBaseClient.create_knowledge_base(\
            client=self.client, name=name, roleArn=role_arn)
        # upload to s3
        # s3_client = S3Client(bucket_name='gt-knowledge-base-documents')
        # if uploaded_files is not None:
        #     for uploaded_file in uploaded_files:
        #         response, message = s3_client.upload_to_s3(uploaded_file=uploaded_file, prefix='apps-billing')
        # create data source
        # dataSourceId = DataSourceClient.create_data_source(client=self.client, name='sdfdsfdsf',\
        #     knowledgeBaseId=knowledgeBaseId, bucket_arn='', prefix='')
        # sync data source
