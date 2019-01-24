import json
import time
import requests
import schedule
from urllib.parse import quote

from charter import Charter


class QQRoutine(Charter):

    charts = {
        'qq_trends': 4,               # 流行指数
        'qq_hot': 26,                 # 热歌
        'qq_new': 27,                 # 新歌
        'qq_original': 52,            # 原创
        }

    def getChart(self, key) -> list:
        '''
        :param chart_id: <int> value of self.charts
        '''
        time.sleep(1)
        chart_id = self.charts[key]
        url = 'https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?'
        params = {}
        params['topid'] = chart_id
        params['song_num'] = 100
        params['format'] = 'json'
        params['platform'] = 'yqq.json'

        try:
            resp = requests.get(url, params=params)
            j = json.loads(resp.content)
            return self.regularize(j['songlist'])
        except Exception:
            return None

    def regularize(self, j):
        '''
        Make QQ data match NetEase format.

        :param j: <list> a list of song_item: dict
        '''
        pos = 0
        for item in j:
            pos += 1

            album_mid = item['data']['albummid']
            song_id = item['data']['songid']
            song_mid = item['data']['songmid']

            song_detail = self.getSongDetail(song_id)['songinfo']['data']['info']

            item['album_url'] = f'https://y.qq.com/n/yqq/album/{album_mid}.html'
            item['album_cover'] = f'https://y.gtimg.cn/music/photo_new/T002R300x300M000{album_mid}.jpg'
            # TODO define this date format
            item['release_date'] = song_detail['pub_time']['content'][0]['value']
            item['album_title'] = item['data']['albumname']
            item['song_pos'] = pos
            item['song_url'] = f'https://y.qq.com/n/yqq/song/{song_mid}.html'
            item['song_title'] = item['data']['songname']
            item['artists'] = []
            for a in item['data']['singer']:
                artist = {'name': a['name']}
                artist['url'] = f'https://y.qq.com/n/yqq/singer/{a["mid"]}.html'
                item['artists'].append(artist)
            item['company'] = []
            for c in song_detail['company']['content']:
                item['company'].append(c['value'])

        return j


    def getSongTitleList(self, key):
        return [i['data']['songname'] for i in self.__dict__[key]]

    def buildHashedList(self, query: list):
        '''
        :param query: <list> search result from MongoDB
        '''
        return hash([i['data']['songname'] for i in query].__str__())

    def getSongDetail(self, song_id):
        '''
        '''
        time.sleep(0.05)
        data = {"songinfo": {
                "method": "get_song_detail_yqq",
                "param": {"song_id": song_id},
                "module": "music.pf_song_detail_svr",
                    }
                }
        d = data.__str__().replace("'", '"')
        url = f'https://u.y.qq.com/cgi-bin/musicu.fcg?data={quote(d)}'
        resp = requests.get(url)
        return json.loads(resp.content)


if __name__ == "__main__":
    QQRoutine()
    schedule.every(3).hours.do(QQRoutine)
    schedule.every().day.at("00:02").do(QQRoutine)
    print(schedule.jobs)
    print('schedule 安排上了')
    while True:
        schedule.run_pending()
        time.sleep(1)
