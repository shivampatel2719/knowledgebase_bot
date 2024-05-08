import boto3

class KnowledgeBaseClient(object):
    
    @staticmethod
    def create_knowledge_base(client, name, roleArn):
        try:
            response = client.create_knowledge_base(
                knowledgeBaseConfiguration={
                    'type': 'VECTOR',
                    'vectorKnowledgeBaseConfiguration': {
                        'embeddingModelArn': 'arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v1'
                    }
                },
                name=name,
                roleArn=roleArn,
                storageConfiguration={
                    'opensearchServerlessConfiguration': {
                        'collectionArn': 'arn:aws:aoss:us-east-1:054244991161:collection/lihtlgw4t6hedic2re4f',
                        'fieldMapping': {
                            'metadataField': 'string',
                            'textField': 'string',
                            'vectorField': 'string'
                        },
                        'vectorIndexName': 'myvectorindex'
                    },
                    'type': 'OPENSEARCH_SERVERLESS'
                },
                tags={
                    'TagSlug': 'GT_KB_EXP'
                }
            )
            if "knowledgeBaseArn" not in response:
                raise Exception(f'KeyError : \'knowledgeBaseArn\' not found in response')
            if "knowledgeBaseId" not in response:
                raise Exception(f'KeyError : \'knowledgeBaseId\' not found in response')
            if "name" not in response:
                raise Exception(f'KeyError : \'name\' not found in response')
            
            return response["name"], response["knowledgeBaseId"], response["knowledgeBaseArn"]
        except Exception as e:
            raise e
        
    @staticmethod
    def list_knowledge_base():
        client = boto3.client('bedrock-agent')
        response = client.list_knowledge_bases()
        return response