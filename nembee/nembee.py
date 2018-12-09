from .api import NetEase
from .utils.tiempo import eightDigits
from .utils.pipeline import MongoDBPipeline


class DailyRoutine():

    n = NetEase()
    RISE = 0                # 云音乐飙升榜
    NEW = 3779629           # 云音乐新歌榜
    ORIGINAL = 2884035      # 网易原创歌曲榜
    HOT = 3778678           # 云音乐热歌榜

    today = eightDigits()

    def __init__(self):
        self.rise = self.getRise()
        self.new = self.getNew()
        self.original = self.getOriginal()
        self.hot = self.getHot()

    def getRise(self):
        return self.n.top_songlist(_id=self.RISE)

    def getNew(self):
        return self.n.top_songlist(_id=self.NEW)

    def getOriginal(self):
        return self.n.top_songlist(_id=self.ORIGINAL)

    def getHot(self):
        return self.n.top_songlist(_id=self.HOT)

    def grab(self):
        pass


class Day():

    today = eightDigits()

    def __init__(self, day=today):
        '''
        Must give 4 lists to call it a day.
        '''


def main():
    pass


if __name__ == "__main__":
    main()
