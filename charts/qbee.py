import time
import schedule

from charter import Charter


class QQRoutine(Charter):

    charts = {
        'qq_trends': 4,               # 流行指数
        'qq_hot': 26,                 # 热歌
        'qq_new': 27,                 # 新歌
        'qq_original': 52,            # 原创
        }

    def getChart(self, key):
        time.sleep(1)
        raise NotImplementedError


if __name__ == "__main__":
    QQRoutine()
    schedule.every(3).hours.do(QQRoutine)
    schedule.every().day.at("00:02").do(QQRoutine)
    print(schedule.jobs)
    print('schedule 安排上了')
    while True:
        schedule.run_pending()
        time.sleep(1)
