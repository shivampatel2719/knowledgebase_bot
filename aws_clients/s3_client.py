import boto3
import boto3
from botocore.exceptions import NoCredentialsError

class S3Client(object):
    def __init__(self, bucket_name) -> None:
        self.client = boto3.client('s3')
        self.bucket_name = bucket_name

    def upload_to_s3(self, uploaded_file, prefix):
        if uploaded_file is not None:
            try:
                self.client.upload_fileobj(uploaded_file, self.bucket_name, f"{prefix}/{uploaded_file.name}")
                return 200, f"File uploaded to S3 bucket {self.bucket_name}: {uploaded_file.name}"
            except NoCredentialsError:
                return 403, f"Upload Access Denied for bucket : {self.bucket_name}"
            except Exception as e:
                return 500, f"An error occurred: {e}"