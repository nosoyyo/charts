import time
import schedule

from api import NetEase
from utils.tiempo import eightDigits
from utils.pipeline import MongoDBPipeline


class Routine():

    m = MongoDBPipeline()
    n = NetEase()
    charts = {
        'rise': 0,                # 云音乐飙升榜
        'new': 3779629,           # 云音乐新歌榜
        'original': 2884035,      # 网易原创歌曲榜
        'hot': 3778678,           # 云音乐热歌榜
        }

    def __init__(self):

        self.today = eightDigits()
        print(self.today)

        try:
            # get the stuff
            for key in self.charts.keys():
                self.__dict__[key] = self.getChart(key)
                print(f'self.{key} grabbed via NetEase API.')
                _hashable = [i['name'] for i in self.__dict__[key]]
                self.__dict__[f'{key}_hash'] = hash(_hashable.__str__())

            # TODO check if not empty
            for key in self.charts.keys():
                self.__dict__[key]

            # check if already in db
            exist_flags = []
            for key in self.charts.keys():
                query = self.m.ls(f'{self.today}.{key}')
                _db_hash = hash([i['name'] for i in query].__str__())

                if _db_hash == self.__dict__[f'{key}_hash']:
                    exist_flags.append(True)
                    print(f'{self.today}.{key} seems already exist.')
                else:
                    exist_flags.append(False)
                    print(f'{self.today}.{key} not there, will insert.')

            # insert into db if nothing exists
            _index = 0
            keys = [key for key in self.charts.keys()]
            for flag in exist_flags:
                if not flag:
                    self.m.db[f'{self.today}.{keys[_index]}'].drop()
                    self.m.db[f'{self.today}.{keys[_index]}'].insert_many(
                                                   self.__dict__[keys[_index]])
                    print(f'{self.today}.{keys[_index]} inserted in MongoDB.')
                _index += 1

        except Exception as e:
            print(e)

    def getChart(self, key):
        time.sleep(1)
        return self.n.top_songlist(_id=self.charts[key])


if __name__ == "__main__":
    Routine()
    schedule.every(3).hours.do(Routine)
    schedule.every().day.at("00:01").do(Routine)
    print(schedule.jobs)
    print('schedule 安排上了')
    while True:
        schedule.run_pending()
        time.sleep(1)
