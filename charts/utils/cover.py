import os
import sys
import logging
import requests
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

from statemgmt import StateManager


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(level=logging.DEBUG)
logger.addHandler(stream_handler)


class CoverToolkits():
    dev_id = os.environ.get('COS_DEV_ID')
    secret_id = os.environ.get('COS_SECRET_ID')
    secret_key = os.environ.get('COS_SECRET_KEY')
    if not dev_id:
        logger.error('no COS_DEV_ID in env')
        raise Exception('must have COS_DEV_ID written in env!')

    region = 'ap-guangzhou'
    config = CosConfig(Region=region,
                       SecretId=secret_id,
                       SecretKey=secret_key,
                       )
    client = CosS3Client(config)

    bucket_nem = f'album-covers-nem-{dev_id}'
    bucket_qq = f'album-covers-qq-{dev_id}'

    @classmethod
    def listBucket(self, which):
        if which == 'nem':
            bucket = self.bucket_nem
        elif which == 'qq':
            bucket = self.bucket_qq
        else:
            raise Exception('only support `nem` or `qq` for now.')
        result = self.client.list_objects(bucket, MaxKeys=999)

        # TODO for later fix when objects over 999
        if result['IsTruncated']:
            logger.warning('Need pagination!')

        try:
            if result['Contents']:
                logger.debug(f'\n{bucket}: {len(result["Contents"])} items\n')
                result = [i['Key'] for i in result['Contents']]
        except KeyError:
            result = None
        return result

    @classmethod
    def storeInCOS(self,
                   nem_id=None,
                   nem_url=None,
                   qq_id=None,
                   qq_url=None):
        '''
        :param url: item['album_cover_original']

        '''
        logger.debug('entering storeInCOS...')
        key = nem_id or qq_id
        url = nem_url or qq_url
        if qq_id:
            bucket = self.bucket_qq
            which = 'qq'
        elif nem_id:
            bucket = self.bucket_nem
            which = 'nem'
        else:
            raise Exception('must contain some id!')
        logger.debug(f'key: {key}\nurl: {url}\nbucket: {bucket}')

        state = StateManager.isCoverExisted(which, key)
        if state:
            if which == 'nem':
                result = self.genCoverURLById(nem_id=key)
            elif which == 'qq':
                result = self.genCoverURLById(qq_id=key)
            else:
                raise Exception('only support `nem` or `qq`!')
            logger.info(f'already exist: {result}')
        else:
            stream = requests.get(url)
            resp = self.client.put_object(
                                    Bucket=bucket,
                                    Body=stream,
                                    Key=f'{key}.jpg',
                                        )
            logger.debug(resp)
            result = f'https://{bucket}.cos.ap-guangzhou.myqcloud.com/{key}.jpg'
            StateManager.coverStored(which, key, result)
            logger.info(f'uploaded: {result}')
        return result

    @classmethod
    def genCoverURLById(self,
                        nem_id=None,
                        qq_id=None):
        key = nem_id or qq_id
        if nem_id:
            bucket = self.bucket_nem
        elif qq_id:
            bucket = self.bucket_qq
        else:
            raise Exception('must contain some id!')
        return f'https://{bucket}.cos.ap-guangzhou.myqcloud.com/{key}.jpg'
