import sys
import redis
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(level=logging.DEBUG)
logger.addHandler(stream_handler)


class StateManager():
    cpool = redis.ConnectionPool(host='localhost',
                                 port=6379,
                                 decode_responses=True,
                                 db=1)

    r = redis.Redis(connection_pool=cpool)

    @classmethod
    def isCoverExisted(self, which, key):
        if which == 'nem':
            q = 'nem_album_covers'
        elif which == 'qq':
            q = 'qq_album_covers'
        else:
            raise Exception('only nem or qq')

        result = self.r.hget(q, key)
        if result:
            logger.info(f'{which} album {key} cover existed.')
            return True
        else:
            logger.info(f'{which} album {key} cover not existed.')
            return False

    @classmethod
    def coverStored(self, which, key, value):
        '''
        :param key: `album_id`
        :param value:   url of `album_cover`
        '''
        if which == 'nem':
            q = 'nem_album_covers'
        elif which == 'qq':
            q = 'qq_album_covers'
        else:
            raise Exception('only nem or qq')

        result = self.r.hset(q, key, value)
        if result:
            logger.info(f'{which} album {key} cover stored.')
            return result
        else:
            logger.error(f'{which} album {key} error when write into redis')
            raise Exception('coverStored state not successfully \
stored in redis! Check StoreManager')
