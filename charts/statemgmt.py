import redis


class StateManager():
    cpool = redis.ConnectionPool(host='localhost',
                                 port=6379,
                                 decode_responses=True,
                                 db=1)

    r = redis.Redis(connection_pool=cpool)

    @classmethod
    def isCoverStored(self, which, key):
        if which == 'nem':
            q = 'nem_album_covers'
        elif which == 'qq':
            q = 'qq_album_covers'
        else:
            raise Exception('only nem or qq')

        result = self.r.hget(q, key)
        if result:
            return True
        else:
            return False
