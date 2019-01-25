import time
import schedule

from nemapi import NetEase
from charter import Charter


class NemRoutine(Charter):

    n = NetEase()
    charts = {
        'nem_rise': 0,                # 云音乐飙升榜
        'nem_new': 3779629,           # 云音乐新歌榜
        'nem_original': 2884035,      # 网易原创歌曲榜
        'nem_hot': 3778678,           # 云音乐热歌榜
        }

    def getChart(self, key) -> list:
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

        pos = 0
        for item in chart:
            pos += 1

            album_id = item['album']['id']
            song_id = item['id']

            item['album_url'] = f'https://music.163.com/album?id={album_id}'
            item['album_cover'] = item['album']['picUrl']
            # TODO define this date format
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
    schedule.every(3).hours.do(NemRoutine)
    schedule.every().day.at("00:01").do(NemRoutine)
    print(schedule.jobs)
    print('schedule 安排上了')
    while True:
        schedule.run_pending()
        time.sleep(1)
