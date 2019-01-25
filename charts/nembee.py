import sys
import time
import logging
import schedule

from nemapi import NetEase
from charter import Charter
from utils.cover import CoverToolkits


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(level=logging.DEBUG)
logger.addHandler(stream_handler)


class NemRoutine(Charter):

    n = NetEase()
    charts = {
        'nem_rise': 0,                # 云音乐飙升榜
        'nem_new': 3779629,           # 云音乐新歌榜
        'nem_original': 2884035,      # 网易原创歌曲榜
        'nem_hot': 3778678,           # 云音乐热歌榜
        }
    nem_bucket_list = CoverToolkits.listBucket('nem')

    def getChart(self, key) -> list:
        logger.debug(f'getChart getting {key}...')
        time.sleep(1)
        chart = self.n.top_songlist(_id=self.charts[key])
        return self.regularize(chart)

    def getSongTitleList(self, key):
        return [i['name'] for i in self.__dict__[key]]

    def buildHashedList(self, query: list):
        '''
        :param query: <list> search result from MongoDB
        '''
        return hash([i['name'] for i in query].__str__())

    def regularize(self, chart):
        '''
        '''
        logger.debug('entering regularize...')
        pos = 0
        for item in chart:
            pos += 1
            logger.debug(f'pos: {pos}')

            album_id = item['album']['id']
            item['album_id'] = album_id
            song_id = item['id']
            item['song_id'] = song_id

            item['album_url'] = f'https://music.163.com/album?id={album_id}'

            item['album_cover_source'] = item['album']['picUrl']
            # storeInCOS will do judge, so just call storeInCOS here
            key = CoverToolkits.storeInCOS(
                nem_id=album_id,
                nem_url=item['album_cover_source'],
                )
            item['album_cover'] = key

            item['release_date'] = item['album']['publishTime']
            item['album_title'] = item['album']['name']
            item['song_pos'] = pos
            item['song_url'] = f'https://music.163.com/song?id={song_id}'
            item['song_title'] = item['name']
            item['artists'] = []
            for a in item['album']['artists']:
                artist = {'name': a['name']}
                artist['url'] = f'https://music.163.com/artist?id={a["id"]}'
                item['artists'].append(artist)
            item['company'] = [item['album']['company']]

        return chart


if __name__ == "__main__":
    NemRoutine()
    schedule.every().day.at("00:01").do(NemRoutine)
    logger.info(schedule.jobs)
    logger.info('schedule 安排上了')
    while True:
        schedule.run_pending()
        time.sleep(1)
