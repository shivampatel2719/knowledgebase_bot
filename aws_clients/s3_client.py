import boto3
import boto3
from botocore.exceptions import NoCredentialsError

class S3Client(object):
    def __init__(self, bucket_name=None) -> None:
        self.client = boto3.client('s3')
        self.bucket_name = bucket_name

    def upload_to_s3(self, bucket_name, uploaded_file, prefix):
        if uploaded_file is not None:
            try:
                self.client.upload_fileobj(uploaded_file, bucket_name, f"{prefix}/{uploaded_file.name}")
                return 200, f"File uploaded to S3 bucket {bucket_name}: {uploaded_file.name}"
            except NoCredentialsError:
                return 403, f"Upload Access Denied for bucket : {bucket_name}"
            except Exception as e:
                return 500, f"An error occurred: {e}"
    
    def get_s3_objects(self, bucket_arn, prefix):
        s3_objects = []
        response = self.client.list_objects_v2(Bucket=bucket_arn, Prefix=prefix)
        response_contents = response.get("Contents")
        for response_content in response_contents:
            if response_content.get("Size") > 0:
                s3_objects.append({
                    "Key": response_content.get("Key"),
                    "ETag": response_content.get("ETag")
                })
        return s3_objects
    
    def delete_s3_object(self, bucket_name, key):
        try:
            self.client.delete_object(Bucket=bucket_name, Key=key)
            return (f"Object '{key}' deleted successfully from bucket '{bucket_name}'")
        except Exception as e:
            return (f"Error deleting object '{key}' from bucket '{bucket_name}': {e}")