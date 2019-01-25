import sys
import logging
from utils.tiempo import eightDigits
from utils.pipeline import MongoDBPipeline


logger = logging.getLogger(__name__)


class Charter():
    '''
    Each inheritor must give a unique prefix for its charts
    '''

    charts = {}
    m = MongoDBPipeline()

    def __init__(self):

        self.today = eightDigits()
        logger.debug(self.today)
        keys = [key for key in self.charts.keys()]
        self.keys = keys

        try:
            # get the stuff
            for key in keys:
                self.__dict__[key] = self.getChart(key)
                logger.info(f'self.{key} grabbed')

                # generate hashes of all song titles of this chart
                _hashable: list = self.getSongTitleList(key)
                self.__dict__[f'{key}_hash'] = hash(_hashable.__str__())

            # check if things are alright
            # self.checkTypes()

            # check if already in db
            exist_flags = []
            for key in keys:
                query = self.m.ls(f'{self.today}.{key}')
                _db_hash = self.buildHashedList(query)

                if _db_hash == self.__dict__[f'{key}_hash']:
                    exist_flags.append(True)
                    logger.info(f'{self.today}.{key} seems already exist.')
                else:
                    exist_flags.append(False)
                    logger.info(f'{self.today}.{key} not there, will insert.')

            # insert into db if nothing exists
            _index = 0
            for flag in exist_flags:
                if not flag:
                    self.m.db[f'{self.today}.{keys[_index]}'].drop()
                    self.m.db[f'{self.today}.{keys[_index]}'].insert_many(
                                                 self.__dict__[keys[_index]])
                    logger.info(
                        f'{self.today}.{keys[_index]} inserted in MongoDB.')
                _index += 1

        except Exception as e:
            logger.error(e)

    def getChart(self, key) -> list:
        raise NotImplementedError

    def getSongTitleList(self, key):
        raise NotImplementedError

    def checkTypes(self):
        for key in self.keys:
            logger.debug(type(self.__dict__[key]))

    def buildHashedList(self, query: list):
        '''
        :param query: <list> search result from MongoDB
        '''
        raise NotImplementedError
