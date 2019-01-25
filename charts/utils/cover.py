import os
import sys
import logging
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

secret_id = os.environ.get('COS_SECRET_ID')
secret_key = os.environ.get('COS_SECRET_KEY')
region = 'ap-guangzhou'
config = CosConfig(Region=region,
                   SecretId=secret_id,
                   SecretKey=secret_key,
                   )

client = CosS3Client(config)
