import json
import time
import requests
import schedule

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
            return self.fixName(j['songlist'])
        except Exception:
            return None

    def getSongTitleList(self, key):
        return [i['data']['songname'] for i in self.__dict__[key]]

    def fixName(self, j: list) -> list:
        '''
        To add the field that the original method needs for processing.
        '''
        for item in j:
            item['name'] = item['data']['songname']
        return j

    def buildHashedList(self, query: list):
        '''
        :param query: <list> search result from MongoDB
        '''
        return hash([i['data']['songname'] for i in query].__str__())


if __name__ == "__main__":
    QQRoutine()
    schedule.every(3).hours.do(QQRoutine)
    schedule.every().day.at("00:02").do(QQRoutine)
    print(schedule.jobs)
    print('schedule 安排上了')
    while True:
        schedule.run_pending()
        time.sleep(1)
