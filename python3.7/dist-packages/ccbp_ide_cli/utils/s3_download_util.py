
from typing import Dict

import boto3


class DownloadFileFromS3Util:

    def __init__(self, s3_credentials: Dict[str, str]):
        self.AWS_STORAGE_BUCKET_NAME = s3_credentials["bucket_name"]
        self.AWS_S3_REGION_NAME = s3_credentials["region_name"]
        self.AWS_ACCESS_KEY_ID = s3_credentials["aws_access_key_id"]
        self.AWS_SECRET_ACCESS_KEY = s3_credentials["secret_access_key"]
        self.AWS_SESSION_TOKEN = s3_credentials["aws_session_token"]

    def download_file_from_private_s3(self, s3_key: str, download_path: str):

        s3 = boto3.resource('s3', region_name=self.AWS_S3_REGION_NAME,
                            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
                            aws_session_token=self.AWS_SESSION_TOKEN)

        s3.Bucket(self.AWS_STORAGE_BUCKET_NAME).download_file(
            s3_key, download_path)
