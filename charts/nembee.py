import time
import schedule

from api import NetEase
from charter import Charter


class NemRoutine(Charter):

    n = NetEase()
    charts = {
        'nem_rise': 0,                # 云音乐飙升榜
        'nem_new': 3779629,           # 云音乐新歌榜
        'nem_original': 2884035,      # 网易原创歌曲榜
        'nem_hot': 3778678,           # 云音乐热歌榜
        }

    def getChart(self, key):
        time.sleep(1)
        return self.n.top_songlist(_id=self.charts[key])


if __name__ == "__main__":
    NemRoutine()
    schedule.every(3).hours.do(NemRoutine)
    schedule.every().day.at("00:01").do(NemRoutine)
    print(schedule.jobs)
    print('schedule 安排上了')
    while True:
        schedule.run_pending()
        time.sleep(1)
