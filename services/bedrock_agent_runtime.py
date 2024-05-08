import random
import boto3

class BedRockAgentRuntime(object):
    '''
        Class for managing bedrock agent for generating responses
        based on knowledge base
    '''
    def __init__(self) -> None:
        self.client = boto3.client('bedrock-agent-runtime')

    def retrieveAndGenerate(self, input, kbId):
        try:
            response = self.client.retrieve_and_generate(
                input={
                    'text': input
                },
                retrieveAndGenerateConfiguration={
                    'type': 'KNOWLEDGE_BASE',
                    'knowledgeBaseConfiguration': {
                        'knowledgeBaseId': kbId,
                        'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0'
                        }
                    }
                )
            if "output" not in response:
                raise Exception('KeyError : \'output\' not found in response')
            if "text" not in response["output"]:
                raise Exception('KeyError : \'text\' not found in response output')
            return response["output"]["text"]
        except Exception as e:
            raise e
